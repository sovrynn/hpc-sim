#!/usr/bin/env python3
import sys
import os

def main():
    # ---------------------------------------
    # Parse arguments
    # ---------------------------------------
    if len(sys.argv) != 2:
        print("Usage: python reverse_values.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    input_file_abs = os.path.abspath(input_file)

    if not os.path.isfile(input_file_abs):
        print(f"Error: input file not found: {input_file}")
        sys.exit(1)

    # ---------------------------------------
    # Prepare output file path
    # ---------------------------------------
    base, ext = os.path.splitext(input_file_abs)
    output_file_abs = base + "-reversed" + ext

    # ---------------------------------------
    # Process file
    # ---------------------------------------
    with open(input_file_abs, 'r') as infile, open(output_file_abs, 'w') as outfile:
        for line in infile:
            parts = line.strip().split()
            if len(parts) < 2:
                continue  # skip malformed lines

            try:
                first = parts[0]
                second = float(parts[1]) * -1  # multiply by -1
                outfile.write(f"{first} {second:.6f}\n")
            except ValueError:
                continue  # skip lines where second is not a number

    print(f"Done. Output written to: {output_file_abs}")

if __name__ == "__main__":
    main()
