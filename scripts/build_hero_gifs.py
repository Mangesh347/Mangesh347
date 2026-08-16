"""Build sequenced hero: GIF1 plays 5x, then GIF2 plays 5x (infinite outer loop)."""
from pathlib import Path
from PIL import Image, ImageSequence

TARGET_W = 640
LOOPS = 5
BG = (13, 17, 23, 255)
QUALITY = 45


def load(path):
    im = Image.open(path)
    frames, durs = [], []
    for fr in ImageSequence.Iterator(im):
        durs.append(max(20, int(fr.info.get("duration", 60) or 60)))
        frames.append(fr.convert("RGBA"))
    return frames, durs


def fit(fr, cw, ch):
    w, h = fr.size
    s = min(cw / w, ch / h)
    nw, nh = max(1, int(w * s)), max(1, int(h * s))
    r = fr.resize((nw, nh), Image.Resampling.BILINEAR)
    c = Image.new("RGBA", (cw, ch), BG)
    c.paste(r, ((cw - nw) // 2, (ch - nh) // 2), r)
    return c


def main():
    f1, d1 = load("GIF 1.gif")
    f2, d2 = load("GIF 2.gif")
    h1 = max(1, int(f1[0].size[1] * TARGET_W / f1[0].size[0]))
    h2 = max(1, int(f2[0].size[1] * TARGET_W / f2[0].size[0]))
    cw, ch = TARGET_W, max(h1, h2)

    # pre-fit once
    a = [fit(fr, cw, ch) for fr in f1]
    b = [fit(fr, cw, ch) for fr in f2]

    seq, durs = [], []
    for _ in range(LOOPS):
        seq.extend(a)
        durs.extend(d1)
    for _ in range(LOOPS):
        seq.extend(b)
        durs.extend(d2)

    out = Path("hero-gifs.webp")
    seq[0].save(
        out,
        save_all=True,
        append_images=seq[1:],
        duration=durs,
        loop=0,
        quality=QUALITY,
        method=0,
    )
    print(f"wrote {out} {out.stat().st_size/1024/1024:.2f} MB {cw}x{ch} frames={len(seq)}")


if __name__ == "__main__":
    main()
