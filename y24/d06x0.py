# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

from __future__ import annotations

import fileinput
from concurrent.futures import ProcessPoolExecutor as Pool
from functools import partial
from operator import add
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

def patrol(G: Grid, pos: Vec2, seen: set[Loc], obstacle=Vec2(-1, -1)) -> bool:
    rot = 0
    while G.is_inbounds(pos) and (pos, rot) not in seen:
        seen.add((pos, rot))
        peek = pos + OFFSETS[rot]
        if G.is_inbounds(peek) and (G[peek] == '#' or peek == obstacle):
            rot = (rot + 1) % 4
        else:
            pos = peek
    return (pos, rot) in seen

def result(G: Grid, pos: Vec2, obstacle: Vec2) -> bool:
    return patrol(G, pos, set(), obstacle)

def obstructions(G: Grid, pos: Vec2, positions: set[Vec2]) -> int:
    with Pool() as pool:
        return sum(pool.map(partial(result, G, pos), positions))

def main():
    G = Grid([*parse(fileinput.input())])
    pos = guard_pos(G)
    locs = set()
    _ = patrol(G, pos + OFFSETS[0], locs)
    positions = {*map(lambda tup: tup[0], locs)}
    ra = len(positions) + (1 if pos not in positions else 0)
    rb = obstructions(G, pos, positions)
    print(ra, rb)

if __name__ == "__main__":
    main()
    raise SystemExit
