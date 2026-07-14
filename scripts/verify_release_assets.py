#!/usr/bin/env python3
"""Verify committed release visual dimensions and animation duration."""

from __future__ import annotations

import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise ValueError(f"not a PNG: {path}")
    return struct.unpack(">II", data[16:24])


def skip_sub_blocks(data: bytes, position: int) -> int:
    while True:
        size = data[position]
        position += 1
        if size == 0:
            return position
        position += size


def gif_info(path: Path) -> tuple[int, int, int, int]:
    data = path.read_bytes()
    if data[:6] not in (b"GIF87a", b"GIF89a"):
        raise ValueError(f"not a GIF: {path}")
    width, height = struct.unpack("<HH", data[6:10])
    packed = data[10]
    position = 13 + (3 * (2 ** ((packed & 0x07) + 1)) if packed & 0x80 else 0)
    delays: list[int] = []
    frames = 0
    while position < len(data):
        marker = data[position]
        position += 1
        if marker == 0x3B:
            break
        if marker == 0x21:
            label = data[position]
            position += 1
            if label == 0xF9:
                size = data[position]
                if size != 4:
                    raise ValueError("invalid GIF graphic control extension")
                delays.append(struct.unpack("<H", data[position + 2 : position + 4])[0])
                position += 1 + size + 1
            else:
                position = skip_sub_blocks(data, position)
        elif marker == 0x2C:
            frames += 1
            descriptor = data[position : position + 9]
            position += 9
            if descriptor[8] & 0x80:
                position += 3 * (2 ** ((descriptor[8] & 0x07) + 1))
            position += 1
            position = skip_sub_blocks(data, position)
        else:
            raise ValueError(f"unexpected GIF marker: 0x{marker:02x}")
    return width, height, frames, sum(delays) * 10


def main() -> None:
    preview = ROOT / "assets/social-preview.png"
    demo = ROOT / "assets/demo.gif"
    if png_size(preview) != (1280, 640):
        raise SystemExit("social preview must be exactly 1280x640")
    width, height, frames, duration_ms = gif_info(demo)
    if (width, height, frames) != (1280, 720, 8) or not 30_000 <= duration_ms <= 45_000:
        raise SystemExit(f"unexpected demo properties: {width}x{height}, {frames} frames, {duration_ms} ms")
    if preview.stat().st_size >= 1_000_000:
        raise SystemExit("social preview exceeds GitHub's 1 MB limit")
    print(f"OK social preview 1280x640 ({preview.stat().st_size} bytes)")
    print(f"OK demo 1280x720, {frames} frames, {duration_ms / 1000:.1f}s")


if __name__ == "__main__":
    main()
