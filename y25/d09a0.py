# {{{
# Copyright 2025, pan (pan_@disroot.org)
# SPDX-License-Identifier: 0BSD

# vi: foldmethod=marker
from __future__ import annotations
from prelude import *

Vec2: TypeAlias = utils.Vec2[int]
# }}}

def parse(itr: Iterator[str]) -> Iterator[Vec2]:
    return map(lambda line: Vec2(*map(int, line.split(','))), itr)

def area(a: Vec2, b: Vec2) -> int:
    dx = abs(b.x - a.x) + 1
    dy = abs(b.y - a.y) + 1
    return dx * dy

def go(inp: Input) -> Iterator[Any]:
    tiles = parse(inp)
    res = max(starmap(area, combinations(tiles, 2)))
    yield res

# {{{
if __name__ == "__main__":
    utils.main(go)
    sys.exit()
# }}}
