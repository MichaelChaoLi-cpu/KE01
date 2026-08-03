# Research Output Issues

## Issues

| # | item | type | severity | description |
|---:|---|---|---|---|
| 1 | figure_minami_ward_shelter_and_cooling_risk_screening.py | script | minor | Accepted non-blocking limitation: the map selects every geolocated row with `Asset Type == shelter` and presents it as a confirmed unavailable shelter without explicitly filtering the planned operational-status, verification-tier, or cooling-loss fields. The two current named records are officially unavailable, so the present result remains valid; no revision is requested for the current research cycle. |
| 2 | Six map-generation scripts | script | minor | Accepted non-blocking limitation: the population, Minami Ward, historical MODIS, functional housing loss, cooling protection, and emergency electricity scripts read the e-Stat administrative-boundary shapefile directly from `data/raw/`. The current results are reproducible with the versioned raw boundary, but boundary processing remains duplicated; no refactoring is requested for the current research cycle. |

## Severity Summary

| severity | count |
|---|---:|
| critical | 0 |
| major | 0 |
| minor | 2 |

## Recommended Next Steps

- 两项 minor 问题已由研究者明确接受为非阻断限制，本轮不再修改。
- 当前不存在需要继续修复的 critical 或 major 问题，可以进行 `build-content-dictionary`。
