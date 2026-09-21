"""Generate the two committed colour-square samples."""

import struct
import zlib
from pathlib import Path


def chunk(kind: bytes, payload: bytes) -> bytes:
    crc = zlib.crc32(kind + payload) & 0xFFFFFFFF
    return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", crc)


def save_png(filename: str, colour: tuple[int, int, int]) -> None:
    size = 100
    pixels = b"".join(b"\0" + bytes(colour) * size for _ in range(size))
    ihdr = struct.pack(">IIBBBBB", size, size, 8, 2, 0, 0, 0)
    data = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(pixels)) + chunk(b"IEND", b"")
    (Path(__file__).parent / filename).write_bytes(data)


save_png("ok.png", (35, 130, 230))
save_png("defect.png", (220, 30, 30))
