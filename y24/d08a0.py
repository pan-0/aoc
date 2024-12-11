# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

from __future__ import annotations

import fileinput
from collections import defaultdict
from operator import add, sub
from itertools import combinations
from typing import NamedTuple

class Vec2(NamedTuple):
    x: int
    y: int

    def __add__(self, other: Vec2) -> Vec2:
        return Vec2(*map(add, self, other))

    def __sub__(self, other: Vec2) -> Vec2:
        return Vec2(*map(sub, self, other))

class Grid:
    def __init__(self, table: list[str]):
        self.rows = len(table)
        self.cols = len(table[0])
        self.table = table

    def is_inbounds(self, vec: Vec2) -> bool:
        return 0 <= vec.x < self.rows and 0 <= vec.y < self.cols

    def __iter__(self):
        return iter(self.table)

def parse(itr) -> Grid:
    return Grid([*map(str.strip, itr)])

Antennas = dict[str, list[Vec2]]

def antennas(G: Grid) -> Antennas:
    A = defaultdict(list)
    for i, row in enumerate(G):
        for j, c in enumerate(row):
            if c != '.':
                A[c].append(Vec2(i, j))
    return A

def f(G: Grid, A: Antennas) -> int:
    antinodes = set()
    for L in A.values():
        for a0, a1 in combinations(L, r=2):
            diff = a1 - a0
            antinodes.update(filter(G.is_inbounds, (a0 - diff, a1 + diff)))
    return len(antinodes)

def main():
    G = parse(fileinput.input())
    A = antennas(G)
    r = f(G, A)
    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit
