#!/usr/bin/env python3
"""Restore a SkyBlog backup archive.

Existing db.sqlite3 and media/ are moved aside with a timestamp before restore.
This makes the operation reversible if the wrong archive is selected.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
import tarfile
import tempfile
from pathlib import Path


def default_project_dir() -> Path:
    return Path(__file__).resolve().parents[1]


def build_parser() -> argparse.ArgumentParser:
    project_dir = default_project_dir()
    parser = argparse.ArgumentParser(description="Restore a SkyBlog backup archive.")
    parser.add_argument("archive", type=Path, help="Path to skyblog-backup-*.tar.gz")
    parser.add_argument(
        "--backend-dir",
        type=Path,
        default=project_dir / "skyblogBackstage",
        help="Path to the Django backend directory.",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Skip confirmation prompt.",
    )
    return parser


def safe_extract(tar: tarfile.TarFile, destination: Path) -> None:
    destination = destination.resolve()

    for member in tar.getmembers():
        member_path = (destination / member.name).resolve()
        if destination != member_path and destination not in member_path.parents:
            raise RuntimeError(f"Unsafe archive path: {member.name}")

    tar.extractall(destination)


def move_aside(path: Path, suffix: str) -> Path | None:
    if not path.exists():
        return None

    backup_path = path.with_name(f"{path.name}.before-restore-{suffix}")
    shutil.move(str(path), str(backup_path))
    return backup_path


def main() -> None:
    args = build_parser().parse_args()
    archive_path = args.archive.resolve()
    backend_dir = args.backend_dir.resolve()

    if not archive_path.exists():
        raise FileNotFoundError(f"Archive not found: {archive_path}")

    if not args.yes:
        answer = input(f"Restore {archive_path} into {backend_dir}? Type YES to continue: ")
        if answer != "YES":
            print("Restore cancelled.")
            return

    timestamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d-%H%M%S")

    with tempfile.TemporaryDirectory(prefix="skyblog-restore-") as temp_name:
        temp_dir = Path(temp_name)

        with tarfile.open(archive_path, "r:gz") as tar:
            safe_extract(tar, temp_dir)

        db_snapshot = temp_dir / "db.sqlite3"
        media_snapshot = temp_dir / "media"
        manifest_path = temp_dir / "manifest.json"

        if not db_snapshot.exists():
            raise RuntimeError("Backup archive does not contain db.sqlite3")

        if manifest_path.exists():
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            print(f"Backup created at: {manifest.get('created_at', 'unknown')}")

        backend_dir.mkdir(parents=True, exist_ok=True)
        old_db = move_aside(backend_dir / "db.sqlite3", timestamp)
        old_media = move_aside(backend_dir / "media", timestamp)

        shutil.copy2(db_snapshot, backend_dir / "db.sqlite3")
        if media_snapshot.exists():
            shutil.copytree(media_snapshot, backend_dir / "media")
        else:
            (backend_dir / "media").mkdir(parents=True, exist_ok=True)

    print("Restore complete.")
    if old_db:
        print(f"Previous database moved to: {old_db}")
    if old_media:
        print(f"Previous media directory moved to: {old_media}")


if __name__ == "__main__":
    main()
