#!/usr/bin/env python3

import argparse
import os
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Rename numerically named images in the current directory so a chosen start index becomes 0."
    )
    parser.add_argument(
        "--start",
        type=int,
        default=7,
        help="First numeric filename to treat as 0 (default: 7).",
    )
    parser.add_argument(
        "-dry",
        action="store_true",
        dest="dry_run",
        help="Print planned renames without changing files.",
    )
    return parser.parse_args()


def numeric_stem(path: Path) -> int:
    try:
        return int(path.stem)
    except ValueError as exc:
        raise ValueError(f"Non-numeric filename found: {path.name}") from exc


def main() -> None:
    args = parse_args()
    directory = Path.cwd().resolve()

    image_paths = sorted(
        [
            path
            for path in directory.iterdir()
            if path.is_file() and path.stem.isdigit()
        ],
        key=numeric_stem,
    )

    if not image_paths:
        raise SystemExit(f"No files found in {directory}")

    rename_pairs = []
    for path in image_paths:
        old_index = numeric_stem(path)
        if old_index < args.start:
            continue
        new_name = f"{old_index - args.start}{path.suffix.lower()}"
        rename_pairs.append((path, directory / new_name))

    if not rename_pairs:
        raise SystemExit(
            f"No files with numeric names greater than or equal to {args.start} were found."
        )

    print(f"Renaming {len(rename_pairs)} files in {directory}:")
    for src, dst in rename_pairs:
        print(f"{src.name} -> {dst.name}")

    if args.dry_run:
        return

    temp_pairs = []
    for index, (src, _) in enumerate(rename_pairs):
        temp_path = directory / f".rename_tmp_{index}{src.suffix.lower()}"
        if temp_path.exists():
            raise SystemExit(f"Temporary file already exists: {temp_path.name}")
        os.rename(src, temp_path)
        temp_pairs.append(temp_path)

    for temp_path, (_, dst) in zip(temp_pairs, rename_pairs):
        if dst.exists():
            raise SystemExit(f"Destination already exists: {dst.name}")
        os.rename(temp_path, dst)


if __name__ == "__main__":
    main()
