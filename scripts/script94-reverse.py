#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path
import shutil

def parse_args():
    parser = argparse.ArgumentParser(
        description="Simply reverse the order of PNG files and save them with the same numbering format."
    )
    parser.add_argument(
        "input_dir",
        help="Relative path to folder containing PNGs (e.g. ./frames)"
    )
    return parser.parse_args()

def main():
    args = parse_args()
    input_dir = Path(args.input_dir).resolve()

    if not input_dir.exists() or not input_dir.is_dir():
        print(f"Error: input folder '{input_dir}' does not exist or is not a directory.", file=sys.stderr)
        sys.exit(1)

    # Collect PNG files, sorted alphabetically
    png_files = sorted(
        [p for p in input_dir.iterdir() if p.is_file() and p.suffix.lower() == ".png"],
        key=lambda p: p.name
    )

    if not png_files:
        print(f"No PNG files found in '{input_dir}'.", file=sys.stderr)
        sys.exit(1)

    num_frames = len(png_files)

    # Determine zero-padding width from existing file names (fallback to 4)
    digit_lengths = []
    for p in png_files:
        stem = p.stem
        if stem.isdigit():
            digit_lengths.append(len(stem))
    pad_width = max(digit_lengths) if digit_lengths else 4

    # Create output directory
    output_dir = input_dir.parent / f"{input_dir.name}-reversed"
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Reversing {num_frames} files...\n")

    for idx, src_path in enumerate(reversed(png_files), start=1):
        dst_name = f"{idx:0{pad_width}d}.png"
        dst_path = output_dir / dst_name

        shutil.copy2(src_path, dst_path)

        print(f"\rCopied {src_path.name} -> {dst_name}", end="", flush=True)

    print("\n\nDone.")

if __name__ == "__main__":
    main()
