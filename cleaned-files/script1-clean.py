#!/usr/bin/env python3
"""
strip_geotiff_metadata.py

Usage:
    python strip_geotiff_metadata.py relative_input.tif

Writes a sanitized copy as ./output.tif that keeps:
- pixels & band count (1 or 3)
- width, height, dtype
- transform / geotransform
- CRS (projection)
- nodata (if present)

Strips everything else: dataset/band tags (EXIF, XML, ICC, GeoTIFF extras),
color tables, per-band odd tags, etc.
"""

import sys
from pathlib import Path
import rasterio
from rasterio.enums import ColorInterp

def main():
    if len(sys.argv) != 2:
        print("Usage: python strip_geotiff_metadata.py relative_input.tif")
        sys.exit(1)

    in_path = Path(sys.argv[1])
    if not in_path.exists():
        print(f"Input not found: {in_path}")
        sys.exit(2)

    out_path = Path("output.tif")

    # Open input read-only; do not trust any tags.
    with rasterio.open(in_path, "r") as src:
        profile = src.profile.copy()

        # Basic essentials we want to preserve
        profile.update(
            driver="GTiff",
            count=src.count,
            dtype=src.dtypes[0],      # assume uniform dtype
            width=src.width,
            height=src.height,
            transform=src.transform,
            crs=src.crs,
            tiled=True,
            compress="DEFLATE",
            # predictor: 3 for float, 2 for integers (helps compression without changing data)
            predictor=3 if "float" in src.dtypes[0].lower() else 2,
            bigtiff="IF_SAFER",
            # Ensure we don’t carry over weird extras implicitly
            photometric=None,   # set below explicitly
        )

        # Decide photometric & color interpretation
        if src.count == 3:
            profile["photometric"] = "RGB"
        elif src.count == 1:
            profile["photometric"] = "MINISBLACK"
        else:
            # If file has an unexpected band count, keep it but don't add extra metadata
            profile["photometric"] = None

        # Remove extras we explicitly *don’t* want to carry over
        for k in ["interleave", "colormap", "axes", "resolution", "blockxsize", "blockysize"]:
            profile.pop(k, None)

        # Recreate a clean file and write only raw data + essentials
        with rasterio.open(out_path, "w", **profile) as dst:
            # Copy pixels band-by-band
            for b in range(1, src.count + 1):
                data = src.read(b)
                dst.write(data, b)

            # Preserve nodata if any (dataset-level or per-band)
            # Prefer dataset-level nodata if set; else check band 1
            nodata = src.nodata
            if nodata is not None:
                dst.nodata = nodata

            # Set color interpretation explicitly (no palettes)
            if src.count == 3:
                dst.colorinterp = (ColorInterp.red, ColorInterp.green, ColorInterp.blue)
            elif src.count == 1:
                dst.colorinterp = (ColorInterp.gray,)
            else:
                # Fall back to undefined for unusual counts
                dst.colorinterp = tuple(ColorInterp.undefined for _ in range(src.count))

            # Wipe dataset- and band-level tags (this is the key “strip” step)
            # NOTE: By not copying tags and explicitly clearing, we drop EXIF/XML/ICC/etc.
            dst.update_tags()  # empty -> clears dataset tags
            for b in range(1, src.count + 1):
                dst.update_tags(b)  # empty -> clears band tags

    print(f"Wrote cleaned GeoTIFF: {out_path.resolve()}")

if __name__ == "__main__":
    main()
