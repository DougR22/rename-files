#!/usr/bin/env python3
"""
Move files from subdirectories into the current working directory. 

Recursively traverses subdirectories, moving files to the root directory. If a file with the same name already exists in the root, it appends a number in parentheses to the filename to avoid overwriting.

Created because HumbleBundle is now packaging files into subdirs and I don't want that.
Created by GPT-6.2 Sol (medium effort mode).
"""

import argparse
import os
from pathlib import Path
import shutil


def available_path(directory: Path, name: str, reserved: set[Path]) -> Path:
    """Find a name that is free on disk and has not been reserved."""
    candidate = directory / name
    original = Path(name)
    number = 1
    # Below candidate.exists() won't work for dry-run, so we also check reserved set.
    while candidate in reserved or candidate.exists() or candidate.is_symlink():
        candidate = directory / f"{original.stem} ({number}){original.suffix}"
        number += 1
    return candidate


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dry-run", action="store_true", help="show moves without changing files"
    )
    args = parser.parse_args()
    root = Path.cwd()
    errors = 0
    moved = 0
    # Track planned names too, so a dry-run reports the same collision handling.
    reserved: set[Path] = set()

    # When I asked Sol for improvements, it suggested this function to handle errors during os.walk.
    def report_scan_error(error: OSError) -> None:
        nonlocal errors
        print(f"Could not scan directory: {error}")
        errors += 1

    for directory, subdirectories, filenames in os.walk(
        root, onerror=report_scan_error, followlinks=False
    ):
        # This includes subdirs of subdirs recursively.
        subdirectories.sort()
        if Path(directory) == root:
            continue
        for name in sorted(filenames):
            source = Path(directory) / name
            destination = available_path(root, name, reserved)
            try:
                if not args.dry_run:
                    shutil.move(str(source), str(destination))
                # When I asked Sol for improvements, it suggested below line move from above the try block to here, in case of move failure.
                reserved.add(destination)
                print(f"{source.relative_to(root)} -> {destination.name}")
                moved += 1
            except OSError as error:
                print(f"Could not move {source}: {error}")
                errors += 1

    action = "Would move" if args.dry_run else "Moved"
    print(f"{action} {moved} file(s); {errors} error(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
