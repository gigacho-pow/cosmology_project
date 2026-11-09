"""네트워크 접근 없이 현재 자료의 해시·행 수와 실행 환경을 기록한다."""

import csv
from datetime import datetime, timezone
import hashlib
from importlib import metadata
import json
from pathlib import Path
import platform
import sys

from download_data import ROOT, SOURCES


def file_record(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "size_bytes": path.stat().st_size,
        "sha256": digest.hexdigest(),
    }


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    recorded_at = datetime.now(timezone.utc).isoformat()
    files = []
    missing = []
    for name, source in SOURCES.items():
        path = ROOT / "data" / name
        if not path.is_file():
            missing.append(name)
            continue
        files.append({**file_record(path), "source_url": source,
                      "source_commit": None, "downloaded_at": None})
    write_json(ROOT / "data/download_manifest.json", {
        "recorded_at_utc": recorded_at,
        "note": "기존 로컬 파일을 검사했다. URL은 기존 다운로드 코드의 출처이며, "
                "실제 다운로드 시각·원격 커밋·원격 파일과의 일치는 확인하지 않았다.",
        "files": files,
        "missing_files": missing,
    })

    galaxy_dir = ROOT / "data/galaxies"
    catalogs = []
    for name, kind in [
        ("sdss_dr18_galaxy_strip.csv", "raw_response"),
        ("sdss_galaxies_with_coordinates.csv", "derived_coordinates"),
    ]:
        path = galaxy_dir / name
        if not path.is_file():
            continue
        with path.open(encoding="utf-8", newline="") as stream:
            reader = csv.DictReader(line for line in stream if not line.startswith("#"))
            columns = reader.fieldnames
            rows = sum(1 for _ in reader)
        catalogs.append({**file_record(path), "kind": kind,
                         "row_count": rows, "columns": columns})
    query = galaxy_dir / "sdss_query.sql"
    if query.exists() or catalogs:
        write_json(galaxy_dir / "catalog_manifest.json", {
            "recorded_at_utc": recorded_at,
            "source_url": "https://skyserver.sdss.org/dr18/SkyServerWS/SearchTools/SqlSearch",
            "downloaded_at": None,
            "query": file_record(query) if query.is_file() else None,
            "files": catalogs,
            "note": "현재 예비 표본은 Dec ±5도 띠이며 넓은 영역 표본은 아직 준비하지 않았다. "
                    "다운로드 시각·서버 반환 완전성·분광 품질 재검증은 미확인이다. "
                    "기존 좌표는 노트북에서 Ωm=0.332, h^-1 Mpc로 계산했다.",
        })

    versions = {}
    for package in ["numpy", "pandas", "matplotlib", "scipy", "scikit-learn",
                    "jupyterlab", "ipykernel"]:
        try:
            versions[package] = metadata.version(package)
        except metadata.PackageNotFoundError:
            versions[package] = None
    write_json(ROOT / "results/runs/environment.json", {
        "recorded_at_utc": recorded_at,
        "python": sys.version,
        "executable": sys.executable,
        "platform": platform.platform(),
        "packages": versions,
        "note": "이 명령을 실행한 인터프리터의 환경이며 기존 노트북 커널과 다를 수 있다.",
    })


if __name__ == "__main__":
    main()
