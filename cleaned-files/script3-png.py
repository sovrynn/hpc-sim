#!/usr/bin/env python3
"""
robust_geotiff_to_geocoded_png.py

Usage:
  python robust_geotiff_to_geocoded_png.py /path/to/input.tif

- Accepts GeoTIFF with 1, 2, 3, or 4 bands (Gray, Gray+A, RGB, RGBA).
- Outputs a PNG next to the input (same basename, .png extension).
- Writes a .pgw world file so the PNG is geocoded (and .aux.xml for projection).
"""

import os
import sys
from osgeo import gdal

def error(msg: str, code: int = 1):
    sys.stderr.write(f"Error: {msg}\n")
    sys.exit(code)

def is_8_or_16bit(dt):
    return dt in (gdal.GDT_Byte, gdal.GDT_UInt16)

def band_type_names(dt):
    return {
        gdal.GDT_Byte: "Byte",
        gdal.GDT_UInt16: "UInt16",
        gdal.GDT_Int16: "Int16",
        gdal.GDT_UInt32: "UInt32",
        gdal.GDT_Int32: "Int32",
        gdal.GDT_Float32: "Float32",
        gdal.GDT_Float64: "Float64",
    }.get(dt, str(dt))

def main():
    if len(sys.argv) != 2:
        error("Provide exactly one input argument: a GeoTIFF file with 1, 2, 3, or 4 bands.")

    in_path = sys.argv[1]
    if not os.path.isfile(in_path):
        error(f"Input file does not exist: {in_path}")

    ds = gdal.Open(in_path, gdal.GA_ReadOnly)
    if ds is None:
        error("Failed to open input with GDAL (is it a valid raster/GeoTIFF?).")

    band_count = ds.RasterCount
    if band_count not in (1, 2, 3, 4):
        error(f"Expected 1, 2, 3, or 4 bands; found {band_count}.")

    # Build band list to copy in order
    band_list = list(range(1, band_count + 1))

    base, _ = os.path.splitext(in_path)
    out_path = base + ".png"

    # Determine a safe output type:
    # If ALL bands are Byte or UInt16, keep the FIRST band's type (typical datasets are uniform).
    # Otherwise, scale to Byte.
    in_types = [ds.GetRasterBand(i).DataType for i in band_list]
    if all(is_8_or_16bit(dt) for dt in in_types):
        # Keep 16-bit if present; otherwise Byte
        out_type = gdal.GDT_UInt16 if any(dt == gdal.GDT_UInt16 for dt in in_types) else gdal.GDT_Byte
        do_scale = False
    else:
        out_type = gdal.GDT_Byte
        do_scale = True

    # If there is a color table on band 1 (paletted raster), don't scale; keep Byte.
    ct = ds.GetRasterBand(1).GetColorTable()
    if ct is not None:
        out_type = gdal.GDT_Byte
        do_scale = False

    # Build scale parameters if needed (per band using min/max)
    scale_params = None
    if do_scale:
        scale_params = []
        for i in band_list:
            b = ds.GetRasterBand(i)
            # Force computation of stats/min/max if not present
            mn, mx = b.ComputeRasterMinMax(True)
            if mn == mx:
                # Avoid divide-by-zero: map flat band to 0 or 255
                mx = mn + 1.0
            # Map [mn, mx] -> [0, 255]
            scale_params.append([mn, mx, 0.0, 255.0])

    # Translate options
    creation_opts = ["WORLDFILE=YES"]  # ensures .pgw is written
    translate_opts = gdal.TranslateOptions(
        format="PNG",
        creationOptions=creation_opts,
        bandList=band_list,
        outputType=out_type,
        # Only set scale if we really need it; otherwise let values pass through unchanged
        scaleParams=scale_params if do_scale else None,
    )

    out_ds = gdal.Translate(out_path, ds, options=translate_opts)
    if out_ds is None:
        error("Failed to create PNG output via gdal.Translate.")

    # Ensure georeferencing is carried over (PNG stores it in sidecars)
    gt = ds.GetGeoTransform(can_return_null=True)
    if gt:
        out_ds.SetGeoTransform(gt)
    proj = ds.GetProjectionRef()
    if proj:
        out_ds.SetProjection(proj)

    # Set sensible color interpretations
    # 1: Gray; 2: Gray+Alpha; 3: R,G,B; 4: R,G,B,Alpha
    if band_count == 1:
        out_ds.GetRasterBand(1).SetColorInterpretation(gdal.GCI_GrayIndex)
    elif band_count == 2:
        out_ds.GetRasterBand(1).SetColorInterpretation(gdal.GCI_GrayIndex)
        out_ds.GetRasterBand(2).SetColorInterpretation(gdal.GCI_AlphaBand)
    elif band_count == 3:
        out_ds.GetRasterBand(1).SetColorInterpretation(gdal.GCI_RedBand)
        out_ds.GetRasterBand(2).SetColorInterpretation(gdal.GCI_GreenBand)
        out_ds.GetRasterBand(3).SetColorInterpretation(gdal.GCI_BlueBand)
    elif band_count == 4:
        out_ds.GetRasterBand(1).SetColorInterpretation(gdal.GCI_RedBand)
        out_ds.GetRasterBand(2).SetColorInterpretation(gdal.GCI_GreenBand)
        out_ds.GetRasterBand(3).SetColorInterpretation(gdal.GCI_BlueBand)
        out_ds.GetRasterBand(4).SetColorInterpretation(gdal.GCI_AlphaBand)

    # If the source had a palette (single-band), preserve it
    if ct is not None and band_count == 1:
        out_ds.GetRasterBand(1).SetColorTable(ct)

    out_ds.FlushCache()
    out_ds = None
    ds = None

    pgw_path = base + ".pgw"
    print(f"Exported geocoded PNG:\n  PNG: {out_path}\n  World file: {pgw_path}")
    print("Projection/CRS is saved in the PAM sidecar (.aux.xml) if needed.")

if __name__ == "__main__":
    # In GDAL 4.0, exceptions are on by default. Enable now to surface clear errors:
    gdal.UseExceptions()
    main()
