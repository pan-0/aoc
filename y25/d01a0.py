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

def go(inp: Input) -> Iterator[Any]:
    dial = 50
    data = parse(inp)
    count = 0
    for rot in data:
        dial = (dial + rot) % 100
        count += dial == 0
    yield count

# {{{
if __name__ == "__main__":
    utils.main(go)
    sys.exit()
# }}}
