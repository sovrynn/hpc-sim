import bpy
import math

# ----------------------------
# Parameters (tweak as needed)
# ----------------------------
SCALE = 67.23       # running-sum scale factor
START_FRAME = 2     # start frame for accumulation
LAST_FRAME = 163     # <--- NEW: last frame to process

# ----------------------------
# Helpers
# ----------------------------
def find_vortex_force():
    """Return the single object that has a VORTEX force field, or None."""
    for obj in bpy.data.objects:
        fld = getattr(obj, "field", None)
        if fld and fld.type == 'VORTEX':
            return obj
    return None

def eval_strength_at_frame(obj, frame):
    """Evaluate the vortex strength at a given frame by setting the scene frame."""
    bpy.context.scene.frame_set(frame)
    return obj.field.strength

# ----------------------------
# Locate scene objects
# ----------------------------
scene = bpy.context.scene
if scene is None:
    raise RuntimeError("No active scene found.")

vortex = find_vortex_force()
if vortex is None:
    raise RuntimeError("Could not find a VORTEX force field object in the scene.")

# ----------------------------
# Accumulate & print rotation curve
# ----------------------------
if START_FRAME < 1:
    START_FRAME = 1

# Ensure LAST_FRAME does not exceed scene.frame_end
frame_end = min(LAST_FRAME, scene.frame_end)

running_sum = 0.0

for f in range(START_FRAME, frame_end + 1):
    val = eval_strength_at_frame(vortex, f)
    running_sum += (val * SCALE)
    
    total_rotation_deg = -running_sum  # Subtractive convention
    
    print(f"{f} {total_rotation_deg:.6f}")

# Optional: restore current frame
# scene.frame_set(scene.frame_current)
