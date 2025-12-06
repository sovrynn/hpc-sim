#!/usr/bin/env python3
import argparse
import os
from pathlib import Path

from PIL import Image  # pip install pillow


def crop_center_square(img: Image.Image, pixel_length: int) -> Image.Image:
    """Crop a centered square of size pixel_length x pixel_length."""
    width, height = img.size
    side = min(pixel_length, width, height)  # clamp if requested size is too big

    left = (width - side) // 2
    top = (height - side) // 2
    right = left + side
    bottom = top + side

    return img.crop((left, top, right, bottom))


def process_folder(input_folder: Path, pixel_length: int) -> None:
    if not input_folder.exists() or not input_folder.is_dir():
        raise FileNotFoundError(f"Input folder does not exist or is not a directory: {input_folder}")

    # Collect PNG files (case-insensitive)
    png_files = sorted(
        [p for p in input_folder.iterdir() if p.is_file() and p.suffix.lower() == ".png"]
    )

    if not png_files:
        print(f"No .png files found in {input_folder}")
        return

    # Output folder: same parent, name + "-cropped"
    output_folder = input_folder.parent / f"{input_folder.name}-cropped"
    output_folder.mkdir(parents=True, exist_ok=True)

    total = len(png_files)
    print(f"Found {total} PNG file(s). Saving cropped images to: {output_folder}\n")

    for idx, in_path in enumerate(png_files, start=1):
        try:
            with Image.open(in_path) as img:
                cropped = crop_center_square(img, pixel_length)

                out_path = output_folder / in_path.name
                cropped.save(out_path)

            # Simple console progress indicator on one line
            progress = idx / total * 100
            print(f"\rProcessing {idx}/{total} ({progress:5.1f}%) - {in_path.name}", end="", flush=True)

        except Exception as e:
            # Move to a new line for error message, then continue
            print(f"\nError processing {in_path}: {e}")

    print("\nDone.")


def main():
    parser = argparse.ArgumentParser(
        description="Crop centered square regions from PNG images in a folder."
    )
    parser.add_argument(
        "input_folder",
        type=str,
        help="Relative path to the folder containing PNG files.",
    )
    parser.add_argument(
        "PIXEL_LENGTH",
        type=int,
        help="Side length (in pixels) of the square crop.",
    )

    args = parser.parse_args()

    input_folder = Path(args.input_folder)
    pixel_length = args.PIXEL_LENGTH

    if pixel_length <= 0:
        raise ValueError("PIXEL_LENGTH must be a positive integer.")

    process_folder(input_folder, pixel_length)


if __name__ == "__main__":
    main()
