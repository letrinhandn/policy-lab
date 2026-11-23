#!/usr/bin/env python3
"""Pack a Quarto post into a complete zip under bundles/.

Includes: index.qmd, config.yaml, README, figures/, scripts/, and other
post files (excluding nested zips, caches, OS junk).

Usage:
  uv run --python 3.12 python scripts/bundle_post.py solow-swan-tang-truong
  uv run --python 3.12 python scripts/bundle_post.py --all
"""
from __future__ import annotations

import argparse
import zipfile
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
POSTS = REPO / "posts"
BUNDLES = REPO / "bundles"

SKIP_NAMES = {".DS_Store", ".gitkeep", "Thumbs.db"}
SKIP_SUFFIXES = {".zip", ".pyc"}
SKIP_DIRS = {"__pycache__", ".ipynb_checkpoints", ".quarto", "_freeze"}


def should_skip(path: Path, root: Path) -> bool:
    rel = path.relative_to(root)
    if any(part in SKIP_DIRS for part in rel.parts):
        return True
    if path.name in SKIP_NAMES:
        return True
    if path.suffix.lower() in SKIP_SUFFIXES:
        return True
    return False


def collect_files(post_dir: Path) -> list[Path]:
    files: list[Path] = []
    for path in sorted(post_dir.rglob("*")):
        if not path.is_file():
            continue
        if should_skip(path, post_dir):
            continue
        files.append(path)
    return files


def bundle_post(slug: str) -> Path:
    post_dir = POSTS / slug
    if not post_dir.is_dir():
        raise SystemExit(f"Post not found: {post_dir}")
    if not (post_dir / "index.qmd").exists():
        raise SystemExit(f"Missing index.qmd in {post_dir}")

    BUNDLES.mkdir(parents=True, exist_ok=True)
    out = BUNDLES / f"{slug}.zip"
    files = collect_files(post_dir)
    if not files:
        raise SystemExit(f"No files to pack in {post_dir}")

    # Root folder inside zip: <slug>/...
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        # Manifest
        listing = "\n".join(f"  {p.relative_to(post_dir).as_posix()}" for p in files)
        manifest = (
            f"Economic Lab post bundle\n"
            f"slug: {slug}\n"
            f"built: {date.today().isoformat()}\n"
            f"files ({len(files)}):\n{listing}\n"
        )
        zf.writestr(f"{slug}/BUNDLE.txt", manifest)
        for path in files:
            arc = f"{slug}/{path.relative_to(post_dir).as_posix()}"
            zf.write(path, arcname=arc)

    size_mb = out.stat().st_size / (1024 * 1024)
    print(f"✓ {out.relative_to(REPO)}  ({len(files)} files, {size_mb:.2f} MB)")
    return out


def list_slugs() -> list[str]:
    slugs = []
    for p in sorted(POSTS.iterdir()):
        if p.name.startswith("_") or not p.is_dir():
            continue
        if (p / "index.qmd").exists():
            slugs.append(p.name)
    return slugs


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slug", nargs="?", help="Post slug under posts/")
    parser.add_argument("--all", action="store_true", help="Bundle every post")
    args = parser.parse_args()

    if args.all:
        slugs = list_slugs()
        if not slugs:
            raise SystemExit("No posts found under posts/")
        for slug in slugs:
            bundle_post(slug)
        return

    if not args.slug:
        raise SystemExit("Provide SLUG or --all")
    bundle_post(args.slug)


if __name__ == "__main__":
    main()
