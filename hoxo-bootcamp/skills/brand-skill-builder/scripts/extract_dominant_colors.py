#!/usr/bin/env python3
"""
Extract dominant colours from one or more images (typically website screenshots).

Returns the top-N colours as hex codes with rough pixel coverage percentages.
Uses PIL's adaptive quantisation — lightweight, fast, and good enough for brand
extraction where we just want "what colours dominate this page".

Usage:
    python extract_dominant_colors.py <image_path> [<image_path> ...] [--n=8]

Output: JSON to stdout, one entry per image, with a list of {hex, rgb, pct} sorted
by coverage descending.

Filtering:
    - Excludes near-white (#F8+ across all channels) unless coverage > 20% (then it's
      almost certainly the brand surface colour, e.g. an off-white).
    - Excludes near-black (#10- across all channels) unless coverage > 5% (likely
      body text colour).
    - Merges colours within 12 RGB units of each other (anti-aliasing artefacts).
"""

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print(json.dumps({"error": "PIL not installed; run: pip install pillow --break-system-packages"}))
    sys.exit(1)


def rgb_to_hex(rgb):
    return "#{:02X}{:02X}{:02X}".format(*rgb)


def is_near_white(rgb, threshold=248):
    return all(c >= threshold for c in rgb)


def is_near_black(rgb, threshold=16):
    return all(c <= threshold for c in rgb)


def color_distance(a, b):
    return sum(abs(x - y) for x, y in zip(a, b))


def merge_close_colors(colors, distance_threshold=36):
    """Merge colours that are within `distance_threshold` total RGB units."""
    merged = []
    for rgb, count in colors:
        for i, (existing_rgb, existing_count) in enumerate(merged):
            if color_distance(rgb, existing_rgb) < distance_threshold:
                # weighted average toward the more-common colour
                new_count = existing_count + count
                new_rgb = tuple(
                    (existing_rgb[c] * existing_count + rgb[c] * count) // new_count
                    for c in range(3)
                )
                merged[i] = (new_rgb, new_count)
                break
        else:
            merged.append((rgb, count))
    return merged


def extract_colors(image_path, n=8, sample_max=600):
    """Return up to n dominant colours."""
    img = Image.open(image_path).convert("RGB")
    # Downsample to reduce noise and speed up
    img.thumbnail((sample_max, sample_max), Image.LANCZOS)

    # Quantise to 64 colours, then count
    quantised = img.quantize(colors=64, method=Image.Quantize.FASTOCTREE)
    palette = quantised.getpalette()  # flat list, 256*3
    color_counts = Counter(quantised.getdata())

    total = sum(color_counts.values())
    raw_colors = []
    for idx, count in color_counts.items():
        rgb = tuple(palette[idx * 3:idx * 3 + 3])
        raw_colors.append((rgb, count))

    # Sort by frequency
    raw_colors.sort(key=lambda x: -x[1])

    # Merge close colours
    merged = merge_close_colors(raw_colors)
    merged.sort(key=lambda x: -x[1])

    # Filter near-white/near-black unless they're dominant
    filtered = []
    for rgb, count in merged:
        pct = 100 * count / total
        if is_near_white(rgb) and pct < 20:
            continue
        if is_near_black(rgb) and pct < 5:
            continue
        filtered.append({
            "hex": rgb_to_hex(rgb),
            "rgb": list(rgb),
            "pct": round(pct, 2),
        })
        if len(filtered) >= n:
            break

    return filtered


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("images", nargs="+")
    ap.add_argument("--n", type=int, default=8, help="max colours per image")
    args = ap.parse_args()

    results = {}
    for path in args.images:
        if not Path(path).exists():
            results[path] = {"error": f"file not found: {path}"}
            continue
        try:
            results[path] = extract_colors(path, n=args.n)
        except Exception as e:
            results[path] = {"error": str(e)}

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
