#!/usr/bin/env python3
import sys
import os

def main():
    # ---------------------------------------
    # Parse arguments
    # ---------------------------------------
    if len(sys.argv) != 2:
        print("Usage: python scale_numbers.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    input_file_abs = os.path.abspath(input_file)

    if not os.path.isfile(input_file_abs):
        print(f"Error: input file not found: {input_file}")
        sys.exit(1)

    # ---------------------------------------
    # Read input lines and extract second numbers
    # ---------------------------------------
    with open(input_file_abs, 'r') as f:
        lines = f.readlines()

    values = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) < 2:
            continue  # Skip malformed lines
        try:
            values.append(float(parts[1]))
        except ValueError:
            continue  # Skip lines where second value isn't a number

    if not values:
        print("Error: No valid numeric second values found in file.")
        sys.exit(1)

    # ---------------------------------------
    # Calculate SCALE
    # ---------------------------------------
    min_val = min(values)
    if min_val == 0:
        print("Error: Smallest value is zero, cannot scale to -104.")
        sys.exit(1)

    SCALE = -104 / min_val
    print(f"Calculated SCALE: {SCALE}")

    # ---------------------------------------
    # Create output filename
    # ---------------------------------------
    base, ext = os.path.splitext(input_file_abs)
    output_file_abs = base + "-scaled" + ext

    # ---------------------------------------
    # Write scaled data
    # ---------------------------------------
    with open(output_file_abs, 'w') as f:
        for line in lines:
            parts = line.strip().split()
            if len(parts) < 2:
                continue

            try:
                first = parts[0]
                second = float(parts[1])
                new_second = second * SCALE
                f.write(f"{first} {new_second:.6f}\n")
            except ValueError:
                continue

    print(f"Done. Scaled file written to: {output_file_abs}")

if __name__ == "__main__":
    main()
