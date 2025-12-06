#!/usr/bin/env python3
import sys
import os
from PIL import Image

def main():
    # ---------------------------------------
    # Parse arguments
    # ---------------------------------------
    if len(sys.argv) != 6:
        print("Usage: python crop_pngs.py <input_folder> <left> <top> <right> <bottom>")
        sys.exit(1)

    input_folder = sys.argv[1]
    try:
        left = int(sys.argv[2])
        top = int(sys.argv[3])
        right = int(sys.argv[4])
        bottom = int(sys.argv[5])
    except ValueError:
        print("Error: left, top, right, bottom must be integers.")
        sys.exit(1)

    # Resolve absolute path for input folder
    input_folder_abs = os.path.abspath(input_folder)
    if not os.path.isdir(input_folder_abs):
        print(f"Error: input folder not found: {input_folder}")
        sys.exit(1)

    # Collect PNG files
    files = sorted(
        f for f in os.listdir(input_folder_abs)
        if f.lower().endswith(".png")
    )

    if not files:
        print("Error: no PNG files found in the input folder.")
        sys.exit(1)

    # ---------------------------------------
    # Prepare output folder
    # ---------------------------------------
    parent_dir = os.path.dirname(input_folder_abs)
    folder_name = os.path.basename(input_folder_abs)
    output_folder_name = folder_name + "-cropped"
    output_folder_abs = os.path.join(parent_dir, output_folder_name)

    os.makedirs(output_folder_abs, exist_ok=True)

    # ---------------------------------------
    # Process each file
    # ---------------------------------------
    total = len(files)

    # Optionally, validate crop box against first image
    first_img_path = os.path.join(input_folder_abs, files[0])
    with Image.open(first_img_path) as first_img:
        w, h = first_img.size
        if not (0 <= left < right <= w and 0 <= top < bottom <= h):
            print(f"Error: crop box ({left}, {top}, {right}, {bottom}) "
                  f"is out of bounds for image size {w}x{h}.")
            sys.exit(1)

    for i, filename in enumerate(files, start=1):
        in_path = os.path.join(input_folder_abs, filename)
        out_path = os.path.join(output_folder_abs, filename)

        # Progress indicator (updates on same line)
        print(f"Processing {i}/{total}: {filename}", end="\r", flush=True)

        with Image.open(in_path) as img:
            # Crop using pixel distances from top-left corner
            cropped = img.crop((left, top, right, bottom))
            cropped.save(out_path)

    # Final newline after progress line
    print()
    print(f"Done. Cropped images written to: {output_folder_abs}")

if __name__ == "__main__":
    main()
