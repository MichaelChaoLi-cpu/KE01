#!/usr/bin/env python3
"""Acquire selected MLIT National Land Numerical Information point datasets for Kumamoto."""

from __future__ import annotations

import argparse
import csv
import hashlib
import shutil
import subprocess
import zipfile
from dataclasses import dataclass
from pathlib import Path


SNAPSHOT_DATE = "2026-08-02"
USER_AGENT = "KE01-kumamoto-rapid-assessment/1.0"


@dataclass(frozen=True)
class Dataset:
    dataset_id: str
    title: str
    reference_year: int
    url: str
    archive_name: str
    license: str
    research_role: str
    limitation: str


DATASETS = (
    Dataset(
        "mlit-ksj-P04-medical-institutions-kumamoto-2020",
        "Medical Institutions",
        2020,
        "https://nlftp.mlit.go.jp/ksj/gml/data/P04/P04-20/P04-20_43_GML.zip",
        "P04-20_43_GML.zip",
        "CC BY 4.0",
        "Medical-support accessibility around exposed grids and shelters.",
        "2020 reference year; includes inactive facilities and does not establish post-earthquake operation.",
    ),
    Dataset(
        "mlit-ksj-P14-welfare-facilities-kumamoto-2023",
        "Welfare Facilities",
        2023,
        "https://nlftp.mlit.go.jp/ksj/gml/data/P14/P14-23/P14-23_43_GML.zip",
        "P14-23_43_GML.zip",
        "CC BY 4.0 with local restrictions",
        "Locate older-person welfare and care resources near exposed populations.",
        "2023 reference year; coverage and local license conditions require verification.",
    ),
    Dataset(
        "mlit-ksj-P05-public-offices-and-halls-kumamoto-2022",
        "Municipal Offices and Public Assembly Facilities",
        2022,
        "https://nlftp.mlit.go.jp/ksj/gml/data/P05/P05-22/P05-22_43_GML.zip",
        "P05-22_43_GML.zip",
        "CC BY 4.0",
        "Candidate public facilities for coordination or temporary cooling-space verification.",
        "2022 reference year; location does not imply shelter designation, cooling, or current availability.",
    ),
    Dataset(
        "mlit-ksj-P29-schools-kumamoto-2023",
        "Schools",
        2023,
        "https://nlftp.mlit.go.jp/ksj/gml/data/P29/P29-23/P29-23_43_GML.zip",
        "P29-23_43_GML.zip",
        "CC BY 4.0",
        "Cross-check school-based shelters and potential large indoor spaces.",
        "2023 reference year; school presence does not establish shelter or HVAC operating status.",
    ),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download(url: str, destination: Path) -> str:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.is_file() and destination.stat().st_size > 0:
        return "kept"
    part = destination.with_suffix(destination.suffix + ".part")
    curl = shutil.which("curl")
    if not curl:
        raise RuntimeError("curl is required")
    result = subprocess.run(
        [
            curl,
            "--fail",
            "--location",
            "--silent",
            "--show-error",
            "--retry",
            "3",
            "--connect-timeout",
            "30",
            "--max-time",
            "180",
            "--user-agent",
            USER_AGENT,
            "--output",
            str(part),
            url,
        ],
        check=False,
    )
    if result.returncode != 0 or not part.is_file() or part.stat().st_size == 0:
        part.unlink(missing_ok=True)
        raise RuntimeError(f"curl failed with exit code {result.returncode}: {url}")
    part.replace(destination)
    return "downloaded"


def extract_flat(archive: Path, destination: Path) -> list[Path]:
    destination.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []
    with zipfile.ZipFile(archive) as bundle:
        for member in bundle.infolist():
            if member.is_dir():
                continue
            name = Path(member.filename).name
            if not name or name in {".", ".."}:
                continue
            target = destination / name
            if not target.is_file() or target.stat().st_size == 0:
                with bundle.open(member) as source, target.open("wb") as output:
                    shutil.copyfileobj(source, output)
            outputs.append(target)
    return sorted(outputs)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()
    raw_root = root / "data/raw/facilities/mlit_ksj_2026-08-02"
    records: list[dict[str, object]] = []

    for dataset in DATASETS:
        dataset_dir = raw_root / dataset.dataset_id
        archive = dataset_dir / dataset.archive_name
        status = download(dataset.url, archive)
        extracted = extract_flat(archive, dataset_dir / "extracted")
        records.append(
            {
                "dataset_id": dataset.dataset_id,
                "title": dataset.title,
                "reference_year": dataset.reference_year,
                "snapshot_date": SNAPSHOT_DATE,
                "source_url": dataset.url,
                "relative_archive": str(archive.relative_to(root)),
                "status": status,
                "archive_bytes": archive.stat().st_size,
                "archive_sha256": sha256(archive),
                "extracted_files": len(extracted),
                "license": dataset.license,
                "research_role": dataset.research_role,
                "limitation": dataset.limitation,
            }
        )
        print(f"{dataset.title}: {status}; extracted {len(extracted)} files")

    manifest = root / "data/raw/_manifests/kumamoto_mlit_ksj_points_2026-08-02.csv"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    with manifest.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)
    print(f"Manifest: {manifest.relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
