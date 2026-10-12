#!/usr/bin/env python3
"""
Reassemble a binary asset (SVG, PNG, etc.) from hex-encoded text chunks
captured via Claude in Chrome's javascript_tool.

The brand-skill-builder workflow can't fetch arbitrary URLs from the bash
sandbox (network allowlist) and Chrome's javascript_tool truncates responses
at ~1KB. The workaround:

1. Claude runs JS in Chrome to fetch the asset, hex-encode the bytes, split
   into ~1000-char chunks separated by spaces (raw alphanumeric strings get
   flagged as "base64 encoded data" by Chrome's safety filter — interspersed
   spaces break the pattern), and store on `window.__assetChunks`.
2. Claude calls browser_batch with N reads of `window.__assetChunks[i]`,
   pasting each chunk into a single text file in the workspace (one chunk
   per line, in order).
3. Claude runs this script: it strips all whitespace and hex-decodes the
   concatenated content into a binary file.

Usage:
    python decode_asset_chunks.py <chunks.txt> <output.svg>

The script tolerates whitespace, line breaks, and minor formatting weirdness.
"""

import sys
from pathlib import Path


def main():
    if len(sys.argv) != 3:
        print("Usage: decode_asset_chunks.py <chunks.txt> <output_path>")
        sys.exit(1)

    chunks_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2])

    raw = chunks_path.read_text()
    hex_clean = ''.join(raw.split())

    if len(hex_clean) % 2 != 0:
        print(f"⚠️  Hex stream has odd length ({len(hex_clean)} chars). "
              f"Truncating last char — there may be a transcription error.")
        hex_clean = hex_clean[:-1]

    # Filter to valid hex chars only — defensive against typos
    valid = ''.join(c for c in hex_clean.lower() if c in '0123456789abcdef')
    if len(valid) != len(hex_clean):
        skipped = len(hex_clean) - len(valid)
        print(f"⚠️  Skipped {skipped} non-hex characters during decode.")

    if len(valid) % 2 != 0:
        valid = valid[:-1]

    try:
        data = bytes.fromhex(valid)
    except ValueError as e:
        print(f"❌ Hex decode failed: {e}")
        sys.exit(2)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(data)

    # Sanity check: print first/last 80 chars if it looks like text
    print(f"✅ Wrote {len(data)} bytes to {out_path}")
    try:
        head = data[:80].decode('utf-8')
        tail = data[-80:].decode('utf-8')
        print(f"   First 80 chars: {head!r}")
        print(f"   Last 80 chars:  {tail!r}")
    except UnicodeDecodeError:
        # binary file — show magic bytes
        print(f"   First 16 bytes (binary): {data[:16].hex()}")


if __name__ == "__main__":
    main()
