# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

from __future__ import annotations

import fileinput
from functools import partial
from operator import add, ne
from typing import NamedTuple

class Vec2(NamedTuple):
    x: int
    y: int

    def __add__(self, other: Vec2) -> Vec2:
        return Vec2(*map(add, self, other))

class Grid:
    def __init__(self, table: list[str]):
        self.rows = len(table)
        self.cols = len(table[0])
        self.table = table

    def is_inbounds(self, vec: Vec2) -> bool:
        return 0 <= vec.x < self.rows and 0 <= vec.y < self.cols

    def __iter__(self):
        return iter(self.table)

    def __getitem__(self, vec: Vec2) -> str:
        return self.table[vec.x][vec.y]

def parse(itr):
    return map(str.strip, itr)

def guard_pos(G: Grid) -> Vec2:
    for i, row in enumerate(G):
        j = row.find('^')
        if j >= 0:
            return Vec2(i, j)
    raise ValueError

OFFSETS = [Vec2(-1,  0),  # Up.
           Vec2( 0,  1),  # Right.
           Vec2(+1,  0),  # Down.
           Vec2( 0, -1)]  # Left.

Loc = tuple[Vec2, int]
Jumps = dict[Loc, Loc]

def patrol(G: Grid, pos: Vec2) -> tuple[set[Vec2], Jumps]:
    seen = set()
    jumps = {}
    rot = 0
    prev = (pos, rot)
    while G.is_inbounds(pos) and (pos, rot) not in seen:
        seen.add((pos, rot))
        peek = pos + OFFSETS[rot]
        if G.is_inbounds(peek) and G[peek] == '#':
            rot = (rot + 1) % 4
            jumps[prev] = prev = (pos, rot)
        else:
            pos = peek
    return seen, jumps

def obstracted_patrol(G: Grid, pos: Vec2, jumps: Jumps, obstacle: Vec2) -> bool:
    seen = set()
    rot = 0
    while G.is_inbounds(pos) and (pos, rot) not in seen:
        seen.add((pos, rot))
        if all(map(ne, pos, obstacle)) and \
                (dest := jumps.get((pos, rot))) is not None:
            pos, rot = dest
        else:
            peek = pos + OFFSETS[rot]
            if G.is_inbounds(peek) and (G[peek] == '#' or peek == obstacle):
                rot = (rot + 1) % 4
            else:
                pos = peek
    return (pos, rot) in seen

def obstructions(G: Grid, pos: Vec2, jumps: Jumps, positions: set[Vec2]) -> int:
    return sum(map(partial(obstracted_patrol, G, pos, jumps), positions))

def main():
    G = Grid([*parse(fileinput.input())])
    pos = guard_pos(G)
    seen, jumps = patrol(G, pos + OFFSETS[0])
    positions = {*map(lambda tup: tup[0], seen)}
    ra = len(positions) + (1 if pos not in positions else 0)
    rb = obstructions(G, pos, jumps, positions)
    print(ra, rb)

if __name__ == "__main__":
    main()
    raise SystemExit
