Just a repo for ECDOsim artifacts.

Mostly renders.

# nit

So, just upload it and then up the domain res. All the forces should be ready to go.

You can render as you go along.

# python venv

venv\Scripts\activate


# windows command to run blender

"C:\Program Files\Blender Foundation\Blender 3.4\blender.exe"

"C:\Program Files\Blender Foundation\Blender 3.6\blender.exe"

"C:\Program Files\Blender Foundation\Blender 4.5\blender.exe"

# ffmpeg

ffmpeg -framerate 1 -i "%04d.png" -pix_fmt yuv420p -c:v libx264 -crf 18 -preset medium out.mp4

ffmpeg -framerate 2 -i "%04d.png" -pix_fmt yuv420p -c:v libx264 -crf 18 -preset medium out.mp4

ffmpeg -framerate 4 -i "%04d.png" -pix_fmt yuv420p -c:v libx264 -crf 18 -preset medium out.mp4

ffmpeg -framerate 8 -i "%04d.png" -pix_fmt yuv420p -c:v libx264 -crf 18 -preset medium out.mp4

ffmpeg -framerate 12 -i "%04d.png" -pix_fmt yuv420p -c:v libx264 -crf 18 -preset medium out.mp4

ffmpeg -framerate 16 -i "%04d.png" -pix_fmt yuv420p -c:v libx264 -crf 18 -preset medium out.mp4

ffmpeg -framerate 12 -i "v10-roraima-final-3884-overlay/%04d.png"  -framerate 12 -i "v10-sulawesi-final-3884-overlay/%04d.png" -filter_complex "hstack=inputs=2" -c:v libx264 -pix_fmt yuv420p output.mp4

# restart windows from terminal

shutdown /r /t 0

# v11

[Vortex | VORTEX] frame 1: strength 0
[Vortex | VORTEX] frame 19.492: strength -0.1206
[Vortex | VORTEX] frame 25.656: strength 0
[Vortex | VORTEX] frame 31.82: strength 0.0402
[Vortex | VORTEX] frame 37.984: strength 0
[Vortex | VORTEX] frame 45.689: strength -0.02412
[Vortex | VORTEX] frame 53.394: strength 0
[Vortex | VORTEX] frame 61.099: strength 0.01206
[Vortex | VORTEX] frame 68.804: strength 0
[Vortex | VORTEX] frame 76.509: strength -0.00804
[Vortex | VORTEX] frame 84.214: strength 0
[Vortex | VORTEX] frame 91.919: strength 0.00402
[Vortex | VORTEX] frame 99.624: strength 0
[Vortex | VORTEX] frame 107.329: strength -0.003216
[Vortex | VORTEX] frame 115.034: strength 0
[Vortex | VORTEX] frame 122.739: strength 0.002412
[Vortex | VORTEX] frame 130.444: strength 0
[Vortex | VORTEX] frame 138.149: strength -0.001608
[Vortex | VORTEX] frame 145.854: strength 0
[Vortex | VORTEX] frame 153.559: strength 0.000804
[Vortex | VORTEX] frame 161.264: strength 0
[Vortex | VORTEX] frame 230.609: strength 0
Object "attractive" not found; skipping.
Object "repulsive" not found; skipping.
Object "inward-squared-force" not found; skipping.
Object "inward-squared-negative" not found; skipping.
Object "in-constant" not found; skipping.
Object "in-constant-negative" not found; skipping.
Object "in-large" not found; skipping.
Object "in-large-negative" not found; skipping.
Object "in-small" not found; skipping.
Object "in-small-negative" not found; skipping.
Object "constant-force" not found; skipping.
[constant | FORCE] frame 1.469: strength 0
[constant | FORCE] frame 26.46: strength -0.067
[constant | FORCE] frame 46.426: strength 0
[constant-negative | FORCE] frame 1.469: strength 0
[constant-negative | FORCE] frame 26.46: strength 0.067
[constant-negative | FORCE] frame 46.426: strength 0
Object "small-force" not found; skipping.
[small | FORCE] frame 1: strength 0
[small | FORCE] frame 19.492: strength -0.0609268
[small | FORCE] frame 31.82: strength -0.0203089
[small | FORCE] frame 45.689: strength -0.0121854
[small | FORCE] frame 61.099: strength -0.00609268
[small | FORCE] frame 76.509: strength -0.00406178
[small | FORCE] frame 91.919: strength -0.00203089
[small | FORCE] frame 107.329: strength -0.00162471
[small | FORCE] frame 122.739: strength -0.00121854
[small | FORCE] frame 138.149: strength -0.000812357
[small | FORCE] frame 153.559: strength -0.000406178
[small | FORCE] frame 161.264: strength 0
[small-negative | FORCE] frame 1: strength -0
[small-negative | FORCE] frame 19.492: strength 0.0609268
[small-negative | FORCE] frame 31.82: strength 0.0203089
[small-negative | FORCE] frame 45.689: strength 0.0121854
[small-negative | FORCE] frame 61.099: strength 0.00609268
[small-negative | FORCE] frame 76.509: strength 0.00406178
[small-negative | FORCE] frame 91.919: strength 0.00203089
[small-negative | FORCE] frame 107.329: strength 0.00162471
[small-negative | FORCE] frame 122.739: strength 0.00121854
[small-negative | FORCE] frame 138.149: strength 0.000812357
[small-negative | FORCE] frame 153.559: strength 0.000406178
[small-negative | FORCE] frame 161.264: strength 0
Object "large-force" not found; skipping.
[large | FORCE] frame 1.469: strength 0
[large | FORCE] frame 26.46: strength -0.1675
[large | FORCE] frame 46.426: strength 0
[large-negative | FORCE] frame 1.469: strength 0
[large-negative | FORCE] frame 26.46: strength 0.1675
[large-negative | FORCE] frame 46.426: strength 0
Object "huge" not found; skipping.
Object "huge-negative" not found; skipping.

# shallow inset

0.01 m thick block in blender gives 1 layer thick @ 700 domain subdivisions

yaa but I don't think I'll be doing that just yet.