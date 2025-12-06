#!/usr/bin/env python3
import sys
import os
from PIL import Image

# ----------------------------------------------------
# Parameters (tweak as needed)
# ----------------------------------------------------
# If NUM_FRAMES is None, process all PNG files.
# Otherwise, process at most NUM_FRAMES files (after sorting alphabetically).
NUM_FRAMES = 30  # e.g. set to 100, or leave as None for all

# ----------------------------------------------------
# Helpers
# ----------------------------------------------------
def find_non_black_bbox(img):
    """
    Find bounding box (left, top, right, bottom) of pixels that are NOT pure black.
    Returns None if all pixels are black.
    """
    img_rgb = img.convert("RGB")
    width, height = img_rgb.size
    pixels = img_rgb.load()

    top = None
    left = None
    right = None
    bottom = None

    # Find top
    for y in range(height):
        for x in range(width):
            if pixels[x, y] != (0, 0, 0):
                top = y
                break
        if top is not None:
            break

    if top is None:
        # Entire image is black
        return None

    # Find bottom
    for y in range(height - 1, -1, -1):
        for x in range(width):
            if pixels[x, y] != (0, 0, 0):
                bottom = y
                break
        if bottom is not None:
            break

    # Find left
    for x in range(width):
        for y in range(height):
            if pixels[x, y] != (0, 0, 0):
                left = x
                break
        if left is not None:
            break

    # Find right
    for x in range(width - 1, -1, -1):
        for y in range(height):
            if pixels[x, y] != (0, 0, 0):
                right = x
                break
        if right is not None:
            break

    return left, top, right, bottom

# ----------------------------------------------------
# Main
# ----------------------------------------------------
def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_directory>")
        sys.exit(1)

    input_dir = sys.argv[1]
    input_dir_abs = os.path.abspath(input_dir)

    if not os.path.isdir(input_dir_abs):
        print(f"Error: directory not found: {input_dir}")
        sys.exit(1)

    # Collect and sort PNG files
    all_files = sorted(
        f for f in os.listdir(input_dir_abs)
        if f.lower().endswith(".png")
    )

    if not all_files:
        print("Error: no PNG files found in the directory.")
        sys.exit(1)

    if NUM_FRAMES is not None and NUM_FRAMES > 0:
        files = all_files[:NUM_FRAMES]
    else:
        files = all_files

    # Global bounding box across all frames
    global_left = None
    global_top = None
    global_right = None
    global_bottom = None

    total = len(files)

    # For sanity, we ensure all frames share the same resolution as the first one
    first_img_path = os.path.join(input_dir_abs, files[0])
    with Image.open(first_img_path) as first_img:
        ref_width, ref_height = first_img.size

    for idx, filename in enumerate(files):
        # Progress indicator
        print(f"Processing {idx + 1}/{total}: {filename}", end="\r", flush=True)

        img_path = os.path.join(input_dir_abs, filename)
        with Image.open(img_path) as img:
            width, height = img.size

            if (width, height) != (ref_width, ref_height):
                print("\nError: not all images have the same resolution.")
                print(f"Mismatch at file: {filename}")
                sys.exit(1)

            bbox = find_non_black_bbox(img)
            if bbox is None:
                # This frame is entirely black; skip
                continue

            left, top, right, bottom = bbox

            if global_left is None:
                # First non-black bbox initializes global bbox
                global_left = left
                global_top = top
                global_right = right
                global_bottom = bottom
            else:
                global_left = min(global_left, left)
                global_top = min(global_top, top)
                global_right = max(global_right, right)
                global_bottom = max(global_bottom, bottom)

    # Finish progress line
    print()  # move to new line

    if global_left is None:
        # All frames are entirely black
        print("0 0 0 0")
    else:
        # Print crop coordinates: left top right bottom
        print(f"{global_left} {global_top} {global_right} {global_bottom}")

if __name__ == "__main__":
    main()
