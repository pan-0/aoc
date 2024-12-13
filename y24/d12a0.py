# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

from __future__ import annotations

import fileinput
from collections import defaultdict
from math import prod
from operator import add, sub
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

    def __getitem__(self, vec: Vec2) -> str:
        return self.table[vec.x][vec.y]

def parse(itr) -> Grid:
    return Grid([*map(str.strip, itr)])

Regions = dict[Vec2, set[Vec2]]

def garden_regions(G: Grid) -> Regions:
    regions = defaultdict(set)
    found = set()
    for i in range(G.rows):
        for j in range(G.cols):
            orig = Vec2(i, j)
            plant = G[orig]
            plots = regions[orig]
            stack = [orig]
            while stack:
                plot = stack.pop()
                if plot not in found and G.is_inbounds(plot) and \
                        G[plot] == plant:
                    found.add(plot)
                    plots.add(plot)
                    stack.extend((plot - Vec2(0, 1),
                                  plot + Vec2(0, 1),
                                  plot - Vec2(1, 0),
                                  plot + Vec2(1, 0)))
    return regions

def perim(region: set[Vec2]) -> int:
    adj = 0
    for plot in region:
        for offs in (Vec2(-1, 0), Vec2(1, 0), Vec2(0, -1), Vec2(0, 1)):
            if plot + offs in region:
                adj += 1
    return 4 * len(region) - adj

def main():
    G = parse(fileinput.input())
    regions = garden_regions(G)
    r = sum(map(prod, zip(map(perim, regions.values()),
                          map(len, regions.values()))))
    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit
