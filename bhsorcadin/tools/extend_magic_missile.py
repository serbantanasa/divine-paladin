#!/usr/bin/env python3
"""Rebuild BHSWI112 as a scaling Magic Missile wrapper.

The stock spell uses five projectile variants for 1..5 missiles. This keeps
those variants in helper spells, then makes BHSWI112 cast helper combinations
for 1..25 missiles at caster levels 1, 3, ..., 49.
"""

from __future__ import annotations

import sys
from pathlib import Path


HEADER_SIZE = 0x72
EXT_SIZE = 0x28
FX_SIZE = 0x30
MAX_MISSILES = 25


def u16(data: bytes | bytearray, off: int) -> int:
    return int.from_bytes(data[off : off + 2], "little")


def u32(data: bytes | bytearray, off: int) -> int:
    return int.from_bytes(data[off : off + 4], "little")


def w16(data: bytearray, off: int, value: int) -> None:
    data[off : off + 2] = value.to_bytes(2, "little")


def w32(data: bytearray, off: int, value: int) -> None:
    data[off : off + 4] = value.to_bytes(4, "little")


def resref(name: str) -> bytes:
    return name.encode("ascii")[:8].ljust(8, b"\0")


def spell_effect(resource: str) -> bytes:
    fx = bytearray(FX_SIZE)
    w16(fx, 0x00, 146)  # Cast Spell
    fx[0x02] = 2  # Preset target
    fx[0x03] = 1  # Power
    w32(fx, 0x08, 1)  # Cast instantly/at target
    fx[0x0c] = 1  # Instant/Permanent
    fx[0x12] = 100
    fx[0x13] = 0
    fx[0x14 : 0x1c] = resref(resource)
    return bytes(fx)


def chunks_for_missiles(total: int) -> list[int]:
    chunks: list[int] = []
    while total > 0:
        chunk = min(5, total)
        chunks.append(chunk)
        total -= chunk
    return chunks


def rebuild_helper(source: bytes, missile_count: int) -> bytes:
    ext_off = u32(source, 0x64)
    feat_off = u32(source, 0x6a)
    cast_count = u16(source, 0x70)

    old_header_off = ext_off + (missile_count - 1) * EXT_SIZE
    old_header = bytearray(source[old_header_off : old_header_off + EXT_SIZE])
    old_fx_index = u16(old_header, 0x20)
    old_fx_count = u16(old_header, 0x1e)

    cast_fx = source[feat_off : feat_off + cast_count * FX_SIZE]
    missile_fx = source[
        feat_off + old_fx_index * FX_SIZE : feat_off + (old_fx_index + old_fx_count) * FX_SIZE
    ]

    new_ext_off = HEADER_SIZE
    new_feat_off = HEADER_SIZE + EXT_SIZE
    header = bytearray(source[:HEADER_SIZE])
    w16(header, 0x1c, 4)
    w32(header, 0x34, 0)
    w32(header, 0x64, new_ext_off)
    w16(header, 0x68, 1)
    w32(header, 0x6a, new_feat_off)

    w16(old_header, 0x02, 4)
    w16(old_header, 0x10, 1)
    w16(old_header, 0x1e, old_fx_count)
    w16(old_header, 0x20, cast_count)

    return bytes(header + old_header + cast_fx + missile_fx)


def rebuild_wrapper(source: bytes) -> bytes:
    ext_off = u32(source, 0x64)
    feat_off = u32(source, 0x6a)
    cast_count = u16(source, 0x70)
    cast_fx = source[feat_off : feat_off + cast_count * FX_SIZE]

    header = bytearray(source[:HEADER_SIZE])
    levels = list(range(1, MAX_MISSILES * 2, 2))
    ext_count = len(levels)
    new_ext_off = HEADER_SIZE
    new_feat_off = HEADER_SIZE + ext_count * EXT_SIZE

    w16(header, 0x1c, 4)
    w32(header, 0x34, 0)
    w32(header, 0x64, new_ext_off)
    w16(header, 0x68, ext_count)
    w32(header, 0x6a, new_feat_off)

    template = bytearray(source[ext_off : ext_off + EXT_SIZE])
    w16(template, 0x02, 4)
    w16(template, 0x26, 1)

    ext_headers = bytearray()
    ability_fx = bytearray()
    fx_index = cast_count
    for missiles, level in enumerate(levels, start=1):
        chunks = chunks_for_missiles(missiles)
        h = bytearray(template)
        w16(h, 0x10, level)
        w16(h, 0x1e, len(chunks))
        w16(h, 0x20, fx_index)
        ext_headers += h
        for chunk in chunks:
            ability_fx += spell_effect(f"BHSMM{chunk}")
        fx_index += len(chunks)

    return bytes(header + ext_headers + cast_fx + ability_fx)


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: extend_magic_missile.py <override-dir>", file=sys.stderr)
        return 2

    override = Path(sys.argv[1])
    source_path = override / "BHSWI112.SPL"
    source = source_path.read_bytes()

    for count in range(1, 6):
        (override / f"BHSMM{count}.SPL").write_bytes(rebuild_helper(source, count))

    source_path.write_bytes(rebuild_wrapper(source))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
