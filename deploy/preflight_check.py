#!/usr/bin/env python3
"""Run SkyBlog release preflight checks.

This script is intentionally conservative: it does not deploy anything. It only
verifies that the frontend builds, Django checks pass, migrations are applied,
static files can be collected, and backup/restore utilities are syntactically
valid.
"""

from __future__ import annotations

import argparse
import os
import platform
import subprocess
import sys
from pathlib import Path


def default_project_dir() -> Path:
    return Path(__file__).resolve().parents[1]


def build_parser() -> argparse.ArgumentParser:
    project_dir = default_project_dir()
    parser = argparse.ArgumentParser(description="Run SkyBlog release preflight checks.")
    parser.add_argument(
        "--project-dir",
        type=Path,
        default=project_dir,
        help="Path to the SkyBlog project root.",
    )
    parser.add_argument(
        "--skip-frontend",
        action="store_true",
        help="Skip npm build.",
    )
    parser.add_argument(
        "--skip-collectstatic",
        action="store_true",
        help="Skip Django collectstatic dry run.",
    )
    parser.add_argument(
        "--deploy-check",
        action="store_true",
        help="Also run Django check --deploy. Warnings are printed but may require HTTPS-specific decisions.",
    )
    return parser


def run_step(title: str, command: list[str], cwd: Path, env: dict[str, str] | None = None) -> None:
    print(f"\n==> {title}")
    print(f"$ {' '.join(command)}")
    completed = subprocess.run(command, cwd=cwd, env=env, check=False)
    if completed.returncode != 0:
        raise SystemExit(f"Step failed: {title} (exit code {completed.returncode})")


def require_path(path: Path, label: str) -> None:
    if not path.exists():
        raise SystemExit(f"Missing {label}: {path}")
    print(f"OK: {label} -> {path}")


def npm_command() -> str:
    return "npm.cmd" if platform.system().lower() == "windows" else "npm"


def python_command() -> list[str]:
    return [sys.executable]


def main() -> None:
    args = build_parser().parse_args()
    project_dir = args.project_dir.resolve()
    backend_dir = project_dir / "skyblogBackstage"
    deploy_dir = project_dir / "deploy"

    print(f"SkyBlog preflight checks for: {project_dir}")
    require_path(project_dir / "package.json", "frontend package.json")
    require_path(backend_dir / "manage.py", "Django manage.py")
    require_path(backend_dir / "requirements.txt", "Django requirements.txt")
    require_path(backend_dir / ".env.example", "Django env template")
    require_path(project_dir / ".env.example", "frontend env template")
    require_path(deploy_dir / "nginx.skyblog.conf.example", "Nginx example config")
    require_path(deploy_dir / "systemd.skyblog.service.example", "systemd example service")

    run_step("Validate backup utility", [*python_command(), "deploy/backup_skyblog.py", "--help"], project_dir)
    run_step("Validate restore utility", [*python_command(), "deploy/restore_skyblog.py", "--help"], project_dir)

    if not args.skip_frontend:
        run_step("Build frontend", [npm_command(), "run", "build"], project_dir)
        require_path(project_dir / "dist" / "index.html", "frontend dist/index.html")

    run_step("Run Django system check", [*python_command(), "manage.py", "check"], backend_dir)
    run_step("Check pending migrations", [*python_command(), "manage.py", "migrate", "--check"], backend_dir)

    if args.deploy_check:
        run_step("Run Django deploy check", [*python_command(), "manage.py", "check", "--deploy"], backend_dir)

    if not args.skip_collectstatic:
        run_step(
            "Collect static files dry run",
            [
                *python_command(),
                "manage.py",
                "collectstatic",
                "--noinput",
                "--dry-run",
                "--clear",
                "--verbosity",
                "0",
            ],
            backend_dir,
        )

    require_path(backend_dir / "db.sqlite3", "SQLite database")
    (backend_dir / "media").mkdir(exist_ok=True)
    require_path(backend_dir / "media", "media directory")

    print("\nPreflight checks passed. This build is ready for a server-side deploy rehearsal.")


if __name__ == "__main__":
    main()
