#!/usr/bin/env python3
"""Historical MODIS and Station-Calibrated Heat Spatial Heterogeneity.

Plan: Show matching-season daytime and nighttime surface heat, retain a
station-calibrated air-temperature surface only when it improves on the
mean-only benchmark out of station, and map prediction uncertainty.
Framework: AnaSOP Section 5 historical spatial heat design, Section 6
cross-validated calibration and population-referenced anomaly equations,
and Section 7 workflow steps 8-10.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from pathlib import Path

import geopandas as gpd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import numpy as np
import pandas as pd
from pyproj import Transformer
from shapely.geometry import LineString


ROOT = Path(__file__).resolve().parents[2]
MODIS_PATH = (
    ROOT
    / "data/processed/kumamoto_modis_historical_heat_spatial_grid_preprocessed.parquet"
)
STATION_PATH = (
    ROOT
    / "data/processed/kumamoto_jma_historical_heat_spatial_stations_preprocessed.parquet"
)
POPULATION_PATH = (
    ROOT / "data/processed/kumamoto_population_mesh_125m_preprocessed.parquet"
)
BOUNDARY_PATH = (
    ROOT / "data/raw/boundaries/estat_2020_small_area_kumamoto/extracted/r2ka43.shp"
)
OUTPUT_PNG = (
    ROOT
    / "data/results/figures/Figure_historical_modis_and_station_calibrated_heat_spatial_heterogeneity.png"
)

MAP_CRS = "EPSG:6670"
GEOGRAPHIC_CRS = "EPSG:4326"
MIN_VALID_OBSERVATIONS = 5
IDW_POWERS = (1.0, 2.0)
IDW_NEIGHBORS = (3, 5, 8)


@dataclass(frozen=True)
class PeriodSpec:
    key: str
    row_label: str
    lst_column: str
    count_column: str
    product_column: str
    target_column: str
    display_lst_column: str
    support_column: str


@dataclass
class CalibrationResult:
    spec: PeriodSpec
    grid: gpd.GeoDataFrame
    stations: gpd.GeoDataFrame
    model_name: str
    supported: bool
    benchmark_rmse: float
    selected_rmse: float
    selected_mae: float
    selected_bias: float
    prediction_column: str
    anomaly_column: str
    uncertainty_column: str
    extrapolation_column: str


PERIODS = (
    PeriodSpec(
        key="daytime",
        row_label="Daytime (daily maximum)",
        lst_column="Historical Daytime Land Surface Temperature C",
        count_column="MODIS Daytime Valid Observation Count",
        product_column="MODIS Daytime Available Product Count",
        target_column="Daily Maximum Air Temperature C",
        display_lst_column=(
            "Coverage-Optimized Historical Daytime Land Surface Temperature C"
        ),
        support_column="Historical Daytime LST Support Tier",
    ),
    PeriodSpec(
        key="nighttime",
        row_label="Nighttime (daily minimum)",
        lst_column="Historical Nighttime Land Surface Temperature C",
        count_column="MODIS Nighttime Valid Observation Count",
        product_column="MODIS Nighttime Available Product Count",
        target_column="Daily Minimum Air Temperature C",
        display_lst_column=(
            "Coverage-Optimized Historical Nighttime Land Surface Temperature C"
        ),
        support_column="Historical Nighttime LST Support Tier",
    ),
)


def rmse(observed: np.ndarray, predicted: np.ndarray) -> float:
    return float(np.sqrt(np.mean((observed - predicted) ** 2)))


def fit_linear(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    design = np.column_stack([np.ones(len(x)), x])
    coefficients, *_ = np.linalg.lstsq(design, y, rcond=None)
    return coefficients


def predict_linear(coefficients: np.ndarray, x: np.ndarray) -> np.ndarray:
    return coefficients[0] + coefficients[1] * x


def idw_predict(
    query_xy: np.ndarray,
    reference_xy: np.ndarray,
    reference_values: np.ndarray,
    power: float,
    neighbors: int,
) -> np.ndarray:
    """Predict values using the nearest inverse-distance-weighted references."""
    delta = query_xy[:, None, :] - reference_xy[None, :, :]
    distances = np.sqrt(np.sum(delta**2, axis=2))
    use_neighbors = min(neighbors, reference_xy.shape[0])
    nearest = np.argpartition(distances, use_neighbors - 1, axis=1)[:, :use_neighbors]
    nearest_distances = np.take_along_axis(distances, nearest, axis=1)
    nearest_values = reference_values[nearest]
    exact = nearest_distances <= 1e-9
    safe_distances = np.maximum(nearest_distances, 1.0)
    weights = safe_distances ** (-power)
    predictions = np.sum(weights * nearest_values, axis=1) / np.sum(weights, axis=1)
    exact_rows = exact.any(axis=1)
    if exact_rows.any():
        exact_position = np.argmax(exact[exact_rows], axis=1)
        predictions[exact_rows] = nearest_values[exact_rows, exact_position]
    return predictions


def candidate_predictions(
    station_xy: np.ndarray,
    lst: np.ndarray,
    target: np.ndarray,
    model_name: str,
) -> np.ndarray:
    """Return leave-one-station-out predictions for one candidate model."""
    predictions = np.full(len(target), np.nan, dtype=float)
    for held_out in range(len(target)):
        train = np.arange(len(target)) != held_out
        if model_name == "mean_only":
            predictions[held_out] = float(np.mean(target[train]))
            continue

        coefficients = fit_linear(lst[train], target[train])
        linear_prediction = float(predict_linear(coefficients, lst[[held_out]])[0])
        if model_name == "satellite_only":
            predictions[held_out] = linear_prediction
            continue

        _, power_text, neighbor_text = model_name.split("_")
        power = float(power_text[1:])
        neighbors = int(neighbor_text[1:])
        residuals = target[train] - predict_linear(coefficients, lst[train])
        residual_prediction = idw_predict(
            station_xy[[held_out]],
            station_xy[train],
            residuals,
            power,
            neighbors,
        )[0]
        predictions[held_out] = linear_prediction + residual_prediction
    return predictions


def fit_predict_surface(
    train_xy: np.ndarray,
    train_lst: np.ndarray,
    train_target: np.ndarray,
    query_xy: np.ndarray,
    query_lst: np.ndarray,
    model_name: str,
) -> np.ndarray:
    if model_name == "mean_only":
        return np.full(len(query_lst), np.mean(train_target), dtype=float)

    coefficients = fit_linear(train_lst, train_target)
    predictions = predict_linear(coefficients, query_lst)
    if model_name == "satellite_only":
        return predictions

    _, power_text, neighbor_text = model_name.split("_")
    power = float(power_text[1:])
    neighbors = int(neighbor_text[1:])
    residuals = train_target - predict_linear(coefficients, train_lst)
    return predictions + idw_predict(
        query_xy,
        train_xy,
        residuals,
        power,
        neighbors,
    )


def graticule_values(lower: float, upper: float, step: float) -> list[float]:
    start = math.ceil((lower - 1e-9) / step) * step
    stop = math.floor((upper + 1e-9) / step) * step
    count = int(round((stop - start) / step)) + 1
    return [round(start + index * step, 8) for index in range(max(0, count))]


def add_graticule(
    ax: plt.Axes,
    geographic_bounds: tuple[float, float, float, float],
    show_longitude_labels: bool,
    show_latitude_labels: bool,
    step: float = 0.25,
) -> None:
    """Draw a labelled longitude/latitude graticule on projected map axes."""
    lon_min, lat_min, lon_max, lat_max = geographic_bounds
    lon_values = graticule_values(lon_min, lon_max, step)
    lat_values = graticule_values(lat_min, lat_max, step)
    samples = 160
    lines: list[LineString] = []
    for longitude in lon_values:
        lines.append(
            LineString(
                zip(
                    np.full(samples, longitude),
                    np.linspace(lat_min - step, lat_max + step, samples),
                    strict=True,
                )
            )
        )
    for latitude in lat_values:
        lines.append(
            LineString(
                zip(
                    np.linspace(lon_min - step, lon_max + step, samples),
                    np.full(samples, latitude),
                    strict=True,
                )
            )
        )
    gpd.GeoSeries(lines, crs=GEOGRAPHIC_CRS).to_crs(MAP_CRS).plot(
        ax=ax,
        color="#7D8992",
        linewidth=0.38,
        linestyle=(0, (2.5, 3.5)),
        alpha=0.52,
        zorder=3,
    )

    transformer = Transformer.from_crs(GEOGRAPHIC_CRS, MAP_CRS, always_xy=True)
    centre_latitude = (lat_min + lat_max) / 2
    centre_longitude = (lon_min + lon_max) / 2
    if show_longitude_labels:
        for longitude in lon_values:
            x_position, _ = transformer.transform(longitude, centre_latitude)
            ax.text(
                x_position,
                -0.012,
                f"{longitude:.2f}°E",
                transform=ax.get_xaxis_transform(),
                ha="center",
                va="top",
                fontsize=6.9,
                color="#3F4A52",
                clip_on=False,
            )
    if show_latitude_labels:
        for latitude in lat_values:
            _, y_position = transformer.transform(centre_longitude, latitude)
            ax.text(
                -0.012,
                y_position,
                f"{latitude:.2f}°N",
                transform=ax.get_yaxis_transform(),
                ha="right",
                va="center",
                fontsize=6.9,
                color="#3F4A52",
                clip_on=False,
            )
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_color("#303A40")
        spine.set_linewidth(0.85)
        spine.set_zorder(10)


def add_scale_bar(ax: plt.Axes, length_km: int = 25) -> None:
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()
    length = length_km * 1_000
    x0 = xmin + 0.055 * (xmax - xmin)
    y0 = ymin + 0.045 * (ymax - ymin)
    ax.plot([x0, x0 + length], [y0, y0], color="#263238", linewidth=2.0, zorder=12)
    ax.plot([x0, x0], [y0 - 700, y0 + 700], color="#263238", linewidth=1.1, zorder=12)
    ax.plot(
        [x0 + length, x0 + length],
        [y0 - 700, y0 + 700],
        color="#263238",
        linewidth=1.1,
        zorder=12,
    )
    ax.text(
        x0 + length / 2,
        y0 + 1_500,
        f"{length_km} km",
        ha="center",
        va="bottom",
        fontsize=7.5,
        color="#263238",
        zorder=12,
    )


def load_inputs() -> tuple[
    gpd.GeoDataFrame,
    pd.DataFrame,
    gpd.GeoDataFrame,
    gpd.GeoDataFrame,
]:
    grid = gpd.read_parquet(MODIS_PATH).to_crs(MAP_CRS)
    station_daily = pd.read_parquet(STATION_PATH)
    population = gpd.read_parquet(POPULATION_PATH).to_crs(MAP_CRS)
    small_areas = gpd.read_file(
        BOUNDARY_PATH, columns=["CITY", "CITY_NAME", "geometry"]
    ).to_crs(MAP_CRS)
    municipalities = small_areas.dissolve(by=["CITY", "CITY_NAME"], as_index=False)
    return grid, station_daily, population, municipalities


def assign_population_to_grid(
    full_grid: gpd.GeoDataFrame,
    population: gpd.GeoDataFrame,
) -> pd.Series:
    """Assign populated 125 m mesh centroids to their containing MODIS pixel."""
    population_points = population[["Total Population", "geometry"]].copy()
    population_points["geometry"] = population_points.geometry.centroid
    joined = gpd.sjoin(
        population_points,
        full_grid[["geometry"]],
        how="inner",
        predicate="within",
    )
    weights = joined.groupby("index_right")["Total Population"].sum()
    assigned = pd.Series(0.0, index=full_grid.index, dtype="float64")
    assigned.loc[weights.index.to_numpy()] = weights.to_numpy(
        dtype="float64", na_value=0.0
    )
    return assigned


def station_targets(station_daily: pd.DataFrame, spec: PeriodSpec) -> gpd.GeoDataFrame:
    required = {
        "Station ID",
        "Station Name",
        "Latitude",
        "Longitude",
        "Temperature Record Complete",
        spec.target_column,
    }
    if missing := required.difference(station_daily.columns):
        raise ValueError(f"Missing station columns: {sorted(missing)}")
    complete = station_daily.loc[
        station_daily["Temperature Record Complete"].eq(True)
        & station_daily[spec.target_column].notna()
    ].copy()
    targets = (
        complete.groupby(
            ["Station ID", "Station Name", "Latitude", "Longitude"],
            as_index=False,
            observed=True,
        )[spec.target_column]
        .mean()
        .rename(columns={spec.target_column: "Station Target Air Temperature C"})
    )
    targets = gpd.GeoDataFrame(
        targets,
        geometry=gpd.points_from_xy(targets["Longitude"], targets["Latitude"]),
        crs=GEOGRAPHIC_CRS,
    ).to_crs(MAP_CRS)
    if len(targets) != 17:
        raise ValueError(f"Expected 17 historical stations, found {len(targets)}")
    return targets


def calibrate_period(
    full_grid: gpd.GeoDataFrame,
    station_daily: pd.DataFrame,
    population_weights: pd.Series,
    spec: PeriodSpec,
) -> CalibrationResult:
    required_grid = {
        spec.lst_column,
        spec.count_column,
        spec.product_column,
        spec.display_lst_column,
        spec.support_column,
        "geometry",
    }
    if missing := required_grid.difference(full_grid.columns):
        raise ValueError(f"Missing MODIS columns: {sorted(missing)}")

    eligible_mask = (
        full_grid[spec.lst_column].notna()
        & full_grid[spec.count_column].ge(MIN_VALID_OBSERVATIONS)
        & full_grid[spec.product_column].eq(2)
    )
    calibration_grid = full_grid.loc[eligible_mask].copy()
    calibration_grid["geometry_centroid"] = calibration_grid.geometry.centroid
    calibration_xy = np.column_stack(
        [
            calibration_grid["geometry_centroid"].x.to_numpy(),
            calibration_grid["geometry_centroid"].y.to_numpy(),
        ]
    )
    calibration_lst = calibration_grid[spec.lst_column].to_numpy(dtype=float)

    display_mask = full_grid[spec.display_lst_column].notna()
    grid = full_grid.loc[display_mask].copy()
    grid["Population Weight"] = population_weights.loc[grid.index].to_numpy()
    grid["LST Low Support"] = grid[spec.support_column].ne("strict_primary")
    grid["geometry_centroid"] = grid.geometry.centroid
    grid_xy = np.column_stack(
        [grid["geometry_centroid"].x.to_numpy(), grid["geometry_centroid"].y.to_numpy()]
    )
    grid_lst = grid[spec.display_lst_column].to_numpy(dtype=float)

    stations = station_targets(station_daily, spec)
    station_xy = np.column_stack([stations.geometry.x, stations.geometry.y])
    distances = np.sqrt(
        np.sum((station_xy[:, None, :] - calibration_xy[None, :, :]) ** 2, axis=2)
    )
    nearest = np.argmin(distances, axis=1)
    stations["Sampled Land Surface Temperature C"] = calibration_lst[nearest]
    stations["Nearest Eligible Pixel Distance m"] = distances[
        np.arange(len(stations)), nearest
    ]
    if stations["Nearest Eligible Pixel Distance m"].max() > 5_000:
        raise ValueError(
            f"A {spec.key} station is more than 5 km from an eligible MODIS pixel."
        )

    station_lst = stations["Sampled Land Surface Temperature C"].to_numpy(dtype=float)
    target = stations["Station Target Air Temperature C"].to_numpy(dtype=float)
    candidate_names = ["mean_only", "satellite_only"] + [
        f"combined_p{power:g}_q{neighbors}"
        for power in IDW_POWERS
        for neighbors in IDW_NEIGHBORS
    ]
    scores: dict[str, dict[str, object]] = {}
    for model_name in candidate_names:
        predictions = candidate_predictions(station_xy, station_lst, target, model_name)
        scores[model_name] = {
            "predictions": predictions,
            "rmse": rmse(target, predictions),
            "mae": float(np.mean(np.abs(target - predictions))),
            "bias": float(np.mean(predictions - target)),
        }

    benchmark_rmse = float(scores["mean_only"]["rmse"])
    satellite_candidates = [name for name in candidate_names if name != "mean_only"]
    selected_name = min(satellite_candidates, key=lambda name: float(scores[name]["rmse"]))
    supported = float(scores[selected_name]["rmse"]) < benchmark_rmse

    prediction_column = "Station-Calibrated Historical Air Temperature C"
    anomaly_column = "Spatial Heat Anomaly C"
    uncertainty_column = "Interpolation Uncertainty C"
    extrapolation_column = "Outside Station LST Range"
    grid[prediction_column] = np.nan
    grid[anomaly_column] = np.nan
    grid[uncertainty_column] = np.nan
    station_min = float(np.min(station_lst))
    station_max = float(np.max(station_lst))
    grid[extrapolation_column] = (grid_lst < station_min) | (grid_lst > station_max)

    if supported:
        surface = fit_predict_surface(
            station_xy,
            station_lst,
            target,
            grid_xy,
            grid_lst,
            selected_name,
        )
        loo_surfaces = []
        for held_out in range(len(target)):
            train = np.arange(len(target)) != held_out
            loo_surfaces.append(
                fit_predict_surface(
                    station_xy[train],
                    station_lst[train],
                    target[train],
                    grid_xy,
                    grid_lst,
                    selected_name,
                )
            )
        surface_sensitivity = np.std(np.vstack(loo_surfaces), axis=0, ddof=1)
        uncertainty = np.sqrt(float(scores[selected_name]["rmse"]) ** 2 + surface_sensitivity**2)
        weights = grid["Population Weight"].to_numpy(dtype=float)
        represented = weights > 0
        if not represented.any():
            raise ValueError("No populated mesh cells were assigned to eligible MODIS pixels.")
        reference = float(np.average(surface[represented], weights=weights[represented]))
        grid[prediction_column] = surface
        grid[anomaly_column] = surface - reference
        grid[uncertainty_column] = uncertainty

    return CalibrationResult(
        spec=spec,
        grid=grid,
        stations=stations,
        model_name=selected_name,
        supported=supported,
        benchmark_rmse=benchmark_rmse,
        selected_rmse=float(scores[selected_name]["rmse"]),
        selected_mae=float(scores[selected_name]["mae"]),
        selected_bias=float(scores[selected_name]["bias"]),
        prediction_column=prediction_column,
        anomaly_column=anomaly_column,
        uncertainty_column=uncertainty_column,
        extrapolation_column=extrapolation_column,
    )


def robust_limits(values: pd.Series, lower: float = 0.02, upper: float = 0.98) -> tuple[float, float]:
    clean = values.dropna()
    return float(clean.quantile(lower)), float(clean.quantile(upper))


def add_horizontal_colorbar(
    fig: plt.Figure,
    ax: plt.Axes,
    mappable: mpl.cm.ScalarMappable,
    label: str,
) -> None:
    bar = fig.colorbar(
        mappable,
        ax=ax,
        orientation="horizontal",
        fraction=0.040,
        pad=0.028,
        extend="both",
    )
    bar.set_label(label, fontsize=7.5, labelpad=2)
    bar.ax.tick_params(labelsize=6.8, length=2.5)


def draw_map(
    fig: plt.Figure,
    ax: plt.Axes,
    layer: gpd.GeoDataFrame,
    column: str,
    cmap: str,
    municipalities: gpd.GeoDataFrame,
    stations: gpd.GeoDataFrame,
    geographic_bounds: tuple[float, float, float, float],
    map_bounds: tuple[float, float, float, float],
    colorbar_label: str,
    show_longitude_labels: bool,
    show_latitude_labels: bool,
    vmin: float | None = None,
    vmax: float | None = None,
    norm: mpl.colors.Normalize | None = None,
    show_extrapolation: bool = False,
) -> None:
    if norm is None:
        if vmin is None or vmax is None:
            vmin, vmax = robust_limits(layer[column])
        norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax, clip=True)
    layer.plot(
        ax=ax,
        column=column,
        cmap=cmap,
        norm=norm,
        linewidth=0,
        rasterized=True,
        zorder=1,
    )
    if show_extrapolation:
        extrapolated = layer.loc[layer["Outside Station LST Range"]]
        if not extrapolated.empty:
            extrapolated.plot(
                ax=ax,
                color="#E6E6E6",
                alpha=0.38,
                linewidth=0,
                rasterized=True,
                zorder=2,
            )
    municipalities.boundary.plot(
        ax=ax,
        color="#525D65",
        linewidth=0.35,
        alpha=0.82,
        zorder=4,
    )
    stations.plot(
        ax=ax,
        marker="o",
        facecolor="white",
        edgecolor="#111111",
        linewidth=0.65,
        markersize=12,
        zorder=5,
    )
    x_padding = 0.025 * (map_bounds[2] - map_bounds[0])
    y_padding = 0.025 * (map_bounds[3] - map_bounds[1])
    ax.set_xlim(map_bounds[0] - x_padding, map_bounds[2] + x_padding)
    ax.set_ylim(map_bounds[1] - y_padding, map_bounds[3] + y_padding)
    ax.set_aspect("equal")
    add_graticule(
        ax,
        geographic_bounds,
        show_longitude_labels=show_longitude_labels,
        show_latitude_labels=show_latitude_labels,
    )
    mappable = mpl.cm.ScalarMappable(norm=norm, cmap=cmap)
    add_horizontal_colorbar(fig, ax, mappable, colorbar_label)


def draw_unsupported_panel(
    ax: plt.Axes,
    municipalities: gpd.GeoDataFrame,
    stations: gpd.GeoDataFrame,
    geographic_bounds: tuple[float, float, float, float],
    map_bounds: tuple[float, float, float, float],
    show_longitude_labels: bool,
    show_latitude_labels: bool,
    message: str,
) -> None:
    municipalities.plot(ax=ax, color="#F1F2F3", edgecolor="none", zorder=1)
    municipalities.boundary.plot(ax=ax, color="#606A72", linewidth=0.35, zorder=3)
    stations.plot(
        ax=ax,
        marker="o",
        facecolor="white",
        edgecolor="#111111",
        linewidth=0.65,
        markersize=12,
        zorder=4,
    )
    x_padding = 0.025 * (map_bounds[2] - map_bounds[0])
    y_padding = 0.025 * (map_bounds[3] - map_bounds[1])
    ax.set_xlim(map_bounds[0] - x_padding, map_bounds[2] + x_padding)
    ax.set_ylim(map_bounds[1] - y_padding, map_bounds[3] + y_padding)
    ax.set_aspect("equal")
    add_graticule(
        ax,
        geographic_bounds,
        show_longitude_labels=show_longitude_labels,
        show_latitude_labels=show_latitude_labels,
    )
    ax.text(
        0.5,
        0.5,
        message,
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=8.2,
        color="#444444",
        bbox={
            "boxstyle": "round,pad=0.3",
            "facecolor": "white",
            "edgecolor": "#888888",
            "linewidth": 0.7,
            "alpha": 0.94,
        },
        zorder=6,
    )


def make_figure(
    results: list[CalibrationResult],
    municipalities: gpd.GeoDataFrame,
) -> plt.Figure:
    mpl.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "figure.facecolor": "white",
            "savefig.facecolor": "white",
        }
    )
    fig, axes = plt.subplots(2, 3, figsize=(15.8, 11.6), constrained_layout=False)
    map_bounds = tuple(municipalities.total_bounds)
    geographic_bounds = tuple(municipalities.to_crs(GEOGRAPHIC_CRS).total_bounds)

    for row, result in enumerate(results):
        is_bottom = row == len(results) - 1
        draw_map(
            fig,
            axes[row, 0],
            result.grid,
            result.spec.display_lst_column,
            "inferno_r",
            municipalities,
            result.stations,
            geographic_bounds,
            map_bounds,
            "Land-surface temperature (°C)",
            show_longitude_labels=is_bottom,
            show_latitude_labels=True,
        )

        if result.supported:
            draw_map(
                fig,
                axes[row, 1],
                result.grid,
                result.prediction_column,
                "RdYlBu_r",
                municipalities,
                result.stations,
                geographic_bounds,
                map_bounds,
                "Station-calibrated air temperature (°C)",
                show_longitude_labels=is_bottom,
                show_latitude_labels=False,
                show_extrapolation=True,
            )
            uncertainty_vmin = float(
                min(
                    item.grid[item.uncertainty_column].quantile(0.02)
                    for item in results
                    if item.supported
                )
            )
            uncertainty_vmax = float(
                max(
                    item.grid[item.uncertainty_column].quantile(0.98)
                    for item in results
                    if item.supported
                )
            )
            draw_map(
                fig,
                axes[row, 2],
                result.grid,
                result.uncertainty_column,
                "YlOrBr",
                municipalities,
                result.stations,
                geographic_bounds,
                map_bounds,
                "Prediction uncertainty (°C)",
                show_longitude_labels=is_bottom,
                show_latitude_labels=False,
                vmin=uncertainty_vmin,
                vmax=uncertainty_vmax,
            )
        else:
            message = (
                "Calibration not supported\n"
                f"satellite RMSE {result.selected_rmse:.2f}°C ≥ "
                f"mean-only {result.benchmark_rmse:.2f}°C"
            )
            draw_unsupported_panel(
                axes[row, 1],
                municipalities,
                result.stations,
                geographic_bounds,
                map_bounds,
                show_longitude_labels=is_bottom,
                show_latitude_labels=False,
                message=message,
            )
            draw_unsupported_panel(
                axes[row, 2],
                municipalities,
                result.stations,
                geographic_bounds,
                map_bounds,
                show_longitude_labels=is_bottom,
                show_latitude_labels=False,
                message="Prediction uncertainty\nnot estimated",
            )

    panel_labels = (
        ("a", "Historical daytime MODIS land-surface temperature"),
        ("b", "Station-calibrated daytime air temperature"),
        ("c", "Daytime prediction uncertainty"),
        ("d", "Historical nighttime MODIS land-surface temperature"),
        ("e", "Station-calibrated nighttime air temperature"),
        ("f", "Nighttime prediction uncertainty"),
    )
    for ax, (letter, label) in zip(axes.flat, panel_labels, strict=True):
        ax.text(
            0.0,
            1.012,
            letter,
            transform=ax.transAxes,
            ha="left",
            va="bottom",
            fontsize=12,
            fontweight="bold",
            color="#20262B",
            clip_on=False,
        )
        ax.text(
            0.055,
            1.012,
            label,
            transform=ax.transAxes,
            ha="left",
            va="bottom",
            fontsize=9.4,
            color="#20262B",
            clip_on=False,
        )

    add_scale_bar(axes[1, 0])
    legend_handles: list[object] = [
        Line2D(
            [0],
            [0],
            marker="o",
            markerfacecolor="white",
            markeredgecolor="#111111",
            markeredgewidth=0.7,
            color="none",
            markersize=5,
            label="JMA station",
        ),
        Patch(
            facecolor="#E6E6E6",
            edgecolor="#888888",
            alpha=0.55,
            label="Outside station-observed LST range",
        ),
    ]
    fig.legend(
        handles=legend_handles,
        loc="lower center",
        bbox_to_anchor=(0.5, 0.012),
        ncol=2,
        frameon=False,
        fontsize=8,
        handlelength=1.7,
        columnspacing=2.3,
    )
    fig.subplots_adjust(
        left=0.055,
        right=0.988,
        top=0.958,
        bottom=0.075,
        wspace=0.09,
        hspace=0.16,
    )
    return fig


def main() -> int:
    grid, station_daily, population, municipalities = load_inputs()
    population_weights = assign_population_to_grid(grid, population)
    results = [
        calibrate_period(grid, station_daily, population_weights, spec)
        for spec in PERIODS
    ]
    figure = make_figure(results, municipalities)
    OUTPUT_PNG.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(OUTPUT_PNG, dpi=400, bbox_inches="tight", facecolor="white")
    plt.close(figure)

    print(f"Saved: {OUTPUT_PNG.relative_to(ROOT)}")
    for result in results:
        status = "supported" if result.supported else "rejected"
        print(
            f"{result.spec.key}: {status}; selected={result.model_name}; "
            f"RMSE={result.selected_rmse:.3f} C; "
            f"mean-only RMSE={result.benchmark_rmse:.3f} C; "
            f"MAE={result.selected_mae:.3f} C; bias={result.selected_bias:.3f} C; "
            f"eligible pixels={len(result.grid):,}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
