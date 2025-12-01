# {{{
# Copyright (C) 2025 by pan <pan_@disroot.org>
# SPDX-License-Identifier: 0BSD

# vi: foldmethod=marker
from __future__ import annotations
from prelude import *

Vec2: TypeAlias = utils.Vec2[int]
dprint = utils.DebugPrint()
# }}}

def parse(itr: Iterator[str]) -> Iterator[Any]:
    return map(lambda line: {'L': -1, 'R': 1}[line[0]] * int(line[1:]),
               filter(bool, itr))

def sign(x):
    return 1 if x >= 0 else -1

def go(inp: Input) -> Iterator[Any]:
    dial = 50
    data = parse(inp)
    count = 0
    for rot in data:
        s = sign(rot)
        for _ in range(abs(rot)):
            dial = (dial + s) % 100
            count += dial == 0
    yield count

# {{{
if __name__ == "__main__":
    utils.main(go)
    sys.exit()
# }}}
