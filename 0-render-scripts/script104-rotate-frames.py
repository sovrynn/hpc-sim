#!/usr/bin/env python3
import sys
import os
from PIL import Image

def parse_rotation_file(rot_file_path):
    """
    Parse the rotation input file.
    Each line: <frame_number> <degrees>
    frame_number is 1-indexed (starting from 2 as per your description).
    Returns a dict: {frame_number: degrees}
    """
    mapping = {}
    with open(rot_file_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            try:
                frame_num = int(parts[0])
                degrees = float(parts[1])
            except ValueError:
                # Skip malformed lines
                continue
            mapping[frame_num] = degrees
    return mapping

def main():
    # ----------------------------------------------------
    # Parse arguments
    # ----------------------------------------------------
    if len(sys.argv) != 3:
        print("Usage: python rotate_frames.py <rotation_file> <input_folder>")
        sys.exit(1)

    rotation_file = sys.argv[1]
    input_folder = sys.argv[2]

    rotation_file_abs = os.path.abspath(rotation_file)
    input_folder_abs = os.path.abspath(input_folder)

    if not os.path.isfile(rotation_file_abs):
        print(f"Error: rotation file not found: {rotation_file}")
        sys.exit(1)

    if not os.path.isdir(input_folder_abs):
        print(f"Error: input folder not found: {input_folder}")
        sys.exit(1)

    # ----------------------------------------------------
    # Parse rotation mapping
    # ----------------------------------------------------
    frame_to_degrees = parse_rotation_file(rotation_file_abs)
    if not frame_to_degrees:
        print("Warning: no valid frame/degrees pairs parsed from rotation file.")

    # ----------------------------------------------------
    # Collect and sort PNG files
    # ----------------------------------------------------
    png_files = sorted(
        f for f in os.listdir(input_folder_abs)
        if f.lower().endswith(".png")
    )

    if not png_files:
        print("Error: no PNG files found in the input folder.")
        sys.exit(1)

    # ----------------------------------------------------
    # Prepare output folder
    # ----------------------------------------------------
    parent_dir = os.path.dirname(input_folder_abs)
    folder_name = os.path.basename(input_folder_abs)
    output_folder_name = folder_name + "-rotated"
    output_folder_abs = os.path.join(parent_dir, output_folder_name)
    os.makedirs(output_folder_abs, exist_ok=True)

    # ----------------------------------------------------
    # Process each image
    # ----------------------------------------------------
    total = len(png_files)
    for idx, filename in enumerate(png_files, start=1):
        frame_number = idx  # frames are 1-indexed with respect to sorted list
        img_path = os.path.join(input_folder_abs, filename)
        out_path = os.path.join(output_folder_abs, filename)

        # Get rotation degrees for this frame
        if frame_number in frame_to_degrees:
            degrees = frame_to_degrees[frame_number]
        else:
            # No rotation specified for this frame.
            # We'll keep it unrotated but still copy it over.
            degrees = 0.0

        with Image.open(img_path) as img:
            # Rotate around center, keep same resolution, crop extras.
            # Pillow's rotate defaults: expand=False (keep size), center=image center.
            if degrees != 0.0:
                rotated = img.rotate(degrees, resample=Image.BICUBIC, expand=False)
            else:
                rotated = img.copy()

            rotated.save(out_path)

        print(f"Frame {frame_number:4d} ({filename}): rotated {degrees} degrees")

    print(f"\nDone. Rotated images written to: {output_folder_abs}")

if __name__ == "__main__":
    main()
