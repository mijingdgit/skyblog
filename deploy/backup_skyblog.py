#!/usr/bin/env python3
"""Create a portable SkyBlog backup archive.

The archive contains:
- a consistent SQLite snapshot of skyblogBackstage/db.sqlite3
- the skyblogBackstage/media directory
- a small manifest.json with backup metadata
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
import sqlite3
import tarfile
import tempfile
from pathlib import Path


def default_project_dir() -> Path:
    return Path(__file__).resolve().parents[1]


def build_parser() -> argparse.ArgumentParser:
    project_dir = default_project_dir()
    parser = argparse.ArgumentParser(description="Back up SkyBlog database and media files.")
    parser.add_argument(
        "--backend-dir",
        type=Path,
        default=project_dir / "skyblogBackstage",
        help="Path to the Django backend directory.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=project_dir / "backups",
        help="Directory where backup archives will be written.",
    )
    parser.add_argument(
        "--keep",
        type=int,
        default=14,
        help="Number of newest backup archives to keep. Use 0 to disable pruning.",
    )
    parser.add_argument(
        "--skip-media",
        action="store_true",
        help="Back up only the SQLite database.",
    )
    return parser


def snapshot_sqlite(source: Path, destination: Path) -> None:
    if not source.exists():
        raise FileNotFoundError(f"Database not found: {source}")

    destination.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(source) as source_connection:
        with sqlite3.connect(destination) as destination_connection:
            source_connection.backup(destination_connection)


def add_directory(tar: tarfile.TarFile, path: Path, arcname: str) -> None:
    if path.exists():
        tar.add(path, arcname=arcname)


def prune_backups(output_dir: Path, keep: int) -> None:
    if keep <= 0:
        return

    archives = sorted(output_dir.glob("skyblog-backup-*.tar.gz"), key=lambda item: item.stat().st_mtime)
    stale_archives = archives[:-keep]
    for archive in stale_archives:
        archive.unlink()


def main() -> None:
    args = build_parser().parse_args()
    backend_dir = args.backend_dir.resolve()
    output_dir = args.output_dir.resolve()
    db_path = backend_dir / "db.sqlite3"
    media_dir = backend_dir / "media"
    timestamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d-%H%M%S")
    archive_path = output_dir / f"skyblog-backup-{timestamp}.tar.gz"

    output_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="skyblog-backup-") as temp_name:
        temp_dir = Path(temp_name)
        snapshot_path = temp_dir / "db.sqlite3"
        manifest_path = temp_dir / "manifest.json"

        snapshot_sqlite(db_path, snapshot_path)

        manifest = {
            "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            "backend_dir": str(backend_dir),
            "database": "db.sqlite3",
            "media_included": not args.skip_media and media_dir.exists(),
        }
        manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

        with tarfile.open(archive_path, "w:gz") as tar:
            tar.add(snapshot_path, arcname="db.sqlite3")
            tar.add(manifest_path, arcname="manifest.json")
            if not args.skip_media:
                add_directory(tar, media_dir, "media")

    prune_backups(output_dir, args.keep)
    size_mb = archive_path.stat().st_size / 1024 / 1024
    print(f"Backup created: {archive_path} ({size_mb:.2f} MB)")


if __name__ == "__main__":
    main()
