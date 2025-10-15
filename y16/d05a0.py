# {{{
# Copyright (C) 2025 by pan <pan_@disroot.org>
# SPDX-License-Identifier: 0BSD

# vi: foldmethod=marker
from __future__ import annotations
from prelude import *

Vec2: TypeAlias = utils.Vec2[int]
dprint = utils.DebugPrint()
# }}}
import hashlib

def go(inp: Input) -> Iterator[str]:
    door = next(inp).strip()
    passw = bytearray()
    index = 0
    for _ in range(8):
        while True:
            key = (door + str(index)).encode("utf-8")
            index += 1
            h = int.from_bytes(islice(hashlib.md5(key).digest(), 3))
            if h & 0xFFFFF0 == 0:
                passw.append(h & 0xF)
                break
    yield "".join(map(lambda c: f"{c:x}", passw))

# {{{
if __name__ == "__main__":
    utils.main(go)
    sys.exit()
# }}}
