"""
Program to rename files in the current directory using 1:1 mappings from 2 txt files:
    1. extract_filenames.txt from extract.py
    2. replace_filenames.txt created by user with new names corresponding to the old names in extract_filenames.txt

This program also validates new filenames against Windows 11 invalid characters.
It also supports dry-run mode.

This program was created by Claude Haiku 4.5 in VSCode.
"""

import os
import argparse

DIRECTORY = os.path.dirname(os.path.abspath(__file__))
EXTRACT_FILE = "extract_filenames.txt"
REPLACE_FILE = "replace_filenames.txt"
LOG_FILE = "rename_log.txt"
VALIDATION_LOG_FILE = "validation_log.txt"
INVALID_CHARS = '<>:"/\\|?*'


def read_lines(filepath):
    if not os.path.isfile(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        return [line.rstrip('\n') for line in f]


def validate_filenames():
    """Check new filenames for invalid Windows characters.

    Prints errors to console and logs to validation_log.txt.
    Returns True if all filenames are valid, False otherwise.
    """
    new_names = read_lines(os.path.join(DIRECTORY, REPLACE_FILE))

    validation_lines = []
    has_errors = False

    for idx, filename in enumerate(new_names):
        if not filename:
            continue

        bad_chars = []
        for pos, char in enumerate(filename):
            if char in INVALID_CHARS:
                bad_chars.append((char, pos))

        if bad_chars:
            has_errors = True
            error_msg = f"Line {idx + 1}: {filename}"
            validation_lines.append(error_msg)
            print(error_msg)

            for char, pos in bad_chars:
                char_detail = f"  Invalid char '{char}' at position {pos}"
                validation_lines.append(char_detail)
                print(char_detail)

    with open(os.path.join(DIRECTORY, VALIDATION_LOG_FILE), 'w', encoding='utf-8') as f:
        for line in validation_lines:
            f.write(line + '\n')
        if not has_errors:
            f.write("All filenames are valid.\n")

    if has_errors:
        print(f"\nValidation errors found. See {VALIDATION_LOG_FILE}")
    else:
        print(f"All filenames validated successfully.")

    return not has_errors


def rename_files(dry_run=True):
    """Perform 1:1 mapping renames for all files.

    Maps old names to new names using extract_filenames.txt and replace_filenames.txt.
    """
    extract_path = os.path.join(DIRECTORY, EXTRACT_FILE)
    replace_path = os.path.join(DIRECTORY, REPLACE_FILE)

    old_names = read_lines(extract_path)
    new_names = read_lines(replace_path)

    try:
        files = [f for f in os.listdir(DIRECTORY) if os.path.isfile(os.path.join(DIRECTORY, f))]
    except FileNotFoundError:
        print(f"Directory not found: {DIRECTORY}")
        return

    log_lines = []
    renamed_count = 0

    for i, old in enumerate(old_names):
        if not old:
            continue

        # Find the file that matches this old name
        filename = None
        for f in files:
            if f == old or f.startswith(old.replace('.pdf', '')):
                filename = f
                break

        if not filename:
            continue

        if i >= len(new_names):
            log_lines.append(f"SKIP {filename}: no corresponding new name at index {i}")
            continue

        new = new_names[i]

        dst_name = filename.replace(old, new, 1)
        src = os.path.join(DIRECTORY, filename)
        dst = os.path.join(DIRECTORY, dst_name)

        if os.path.exists(dst):
            log_lines.append(f"CONFLICT {filename} -> {dst_name}")
            continue

        if dry_run:
            log_lines.append(f"DRY_RUN {filename} -> {dst_name}")
            renamed_count += 1
        else:
            try:
                os.rename(src, dst)
                log_lines.append(f"RENAMED {filename} -> {dst_name}")
                renamed_count += 1
            except Exception as e:
                error_msg = f"ERROR {filename}: {e}"
                log_lines.append(error_msg)
                print(error_msg.upper())

    with open(os.path.join(DIRECTORY, LOG_FILE), 'w', encoding='utf-8') as f:
        for line in log_lines:
            f.write(line + '\n')

    status = "DRY RUN - renames not applied" if dry_run else "Applied"
    print(f"Processed {len(old_names)} entries. {renamed_count} files. {status}. Log: {LOG_FILE}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Rename files using 1:1 mappings')
    parser.add_argument('--apply', action='store_true', help='Apply renames (default: dry-run)')
    args = parser.parse_args()

    if not validate_filenames():
        print("Fix validation errors before proceeding.")
        exit(1)

    rename_files(dry_run=not args.apply)
