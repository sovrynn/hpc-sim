#!/usr/bin/env python3
import argparse
from pathlib import Path

from PIL import Image  # pip install pillow


def fill_with_black_background(img: Image.Image) -> Image.Image:
    """
    Take an image (possibly with transparency) and return a new image of the
    same size with a black background and the original image composited on top.
    """
    # Ensure we have RGBA so there's an alpha channel to work with
    rgba = img.convert("RGBA")
    width, height = rgba.size

    # Create a black background (opaque)
    background = Image.new("RGBA", (width, height), (0, 0, 0, 255))

    # Composite original onto black background using its alpha
    composed = Image.alpha_composite(background, rgba)

    # Drop alpha (no longer needed) -> RGB
    return composed.convert("RGB")


def process_folder(input_folder: Path) -> None:
    if not input_folder.exists() or not input_folder.is_dir():
        raise FileNotFoundError(f"Input folder does not exist or is not a directory: {input_folder}")

    png_files = sorted(
        [p for p in input_folder.iterdir() if p.is_file() and p.suffix.lower() == ".png"]
    )

    if not png_files:
        print(f"No .png files found in {input_folder}")
        return

    output_folder = input_folder.parent / f"{input_folder.name}-filled"
    output_folder.mkdir(parents=True, exist_ok=True)

    total = len(png_files)
    print(f"Found {total} PNG file(s). Writing filled images to: {output_folder}\n")

    for idx, in_path in enumerate(png_files, start=1):
        try:
            with Image.open(in_path) as img:
                filled = fill_with_black_background(img)
                out_path = output_folder / in_path.name
                filled.save(out_path, format="PNG")

            # Simple console progress indicator
            progress = idx / total * 100
            print(f"\rProcessing {idx}/{total} ({progress:5.1f}%) - {in_path.name}", end="", flush=True)

        except Exception as e:
            print(f"\nError processing {in_path}: {e}")

    print("\nDone.")


def main():
    parser = argparse.ArgumentParser(
        description="Overlay PNGs with transparency onto a black background and save to a new folder."
    )
    parser.add_argument(
        "input_folder",
        type=str,
        help="Relative path to the folder containing PNG files.",
    )

    args = parser.parse_args()
    input_folder = Path(args.input_folder)
    process_folder(input_folder)


if __name__ == "__main__":
    main()
