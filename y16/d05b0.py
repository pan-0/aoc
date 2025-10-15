# {{{
# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

# vi: foldmethod=marker
from __future__ import annotations
from prelude import *

Vec2: TypeAlias = utils.Vec2[int]
dprint = utils.DebugPrint()
# }}}
import hashlib

def go(inp: Input) -> Iterator[str]:
    door = next(inp).strip()
    bitmap = 0xFF00
    passw = bytearray((0,) * 8)
    index = 0
    for _ in range(8):
        while True:
            key = (door + str(index)).encode("utf-8")
            index += 1
            h = int.from_bytes(islice(hashlib.md5(key).digest(), 4))
            if h & 0xFFFFF000 == 0:
                pos = (h >> 8) & 0xF
                if (bitmap >> pos) & 1 == 0:
                    bitmap |= 1 << pos
                    ch = (h >> 4) & 0xF
                    passw[pos] = ch
                    break
    yield "".join(map(lambda c: f"{c:x}", passw))

# {{{
if __name__ == "__main__":
    utils.main(go)
    sys.exit()
# }}}
