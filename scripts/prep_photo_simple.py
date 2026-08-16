"""
Prep Mangesh's portrait for ASCII: flood-fill the dark burnt-orange studio
backdrop to white so it becomes blank space in the ASCII ramp.
"""
import os
import sys
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
INP = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "source-photo.jpg")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "source-prepped.png")

im = Image.open(INP).convert("RGB")
im.thumbnail((900, 1200), Image.LANCZOS)
arr = np.array(im).astype(np.int16)
h, w = arr.shape[:2]

# crop a portrait-ish frame (keep head + shoulders)
new_w = int(h * 0.72)
left = max(0, (w - new_w) // 2)
arr = arr[:, left:left + new_w]
h, w = arr.shape[:2]

ref = arr[8, 8]
dist = np.abs(arr - ref).sum(axis=2)
# warm dark backdrop, not skin (skin is near-gray) and not black shirt
warm = (arr[:, :, 0] > arr[:, :, 2] + 18) & (arr[:, :, 0] > arr[:, :, 1] + 8)
mask = (dist < 140) & warm

# also grab near-black corners of the frame if they match the backdrop falloff
edge = np.zeros((h, w), dtype=bool)
edge[:12, :] = True
edge[:, :12] = True
edge[:, -12:] = True
mask = mask | ((dist < 90) & edge)

out = arr.copy()
out[mask] = 255
gray = Image.fromarray(out.astype(np.uint8), "RGB").convert("L")
gray = ImageOps.autocontrast(gray, cutoff=1)
gray = ImageEnhance.Contrast(gray).enhance(1.2)
gray = ImageEnhance.Brightness(gray).enhance(1.15)
gray.save(OUT)
print("wrote", OUT, gray.size, "bg keyed", int(mask.mean() * 100), "%")
