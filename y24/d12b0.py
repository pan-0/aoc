# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

from __future__ import annotations

import fileinput
import utils

from collections import defaultdict
from itertools import takewhile
from math import prod
from utils import Adjacents

Grid = utils.Grid[str]
Vec2 = utils.Vec2[int]

dprint = utils.DebugPrint()

def parse(itr) -> Grid:
    return Grid([*map(str.strip, takewhile(lambda line: line != "\n", itr))])

Regions = list[set[Vec2]]

def garden_regions(G: Grid) -> Regions:
    regions = []
    found = set()
    for i in range(G.rows):
        for j in range(G.cols):
            orig = Vec2(j, i)
            plant = G[orig]

            region = set()
            for plot in G.dfs(orig,
                              key=lambda x: x not in found and G[x] == plant,
                              adj=G.adjacent_cross):
                found.add(plot)
                region.add(plot)

            if region:
                regions.append(region)

    return regions

def sides(region: set[Vec2]) -> int:
    count = 0
    for rev, vec, step in ((True,  Vec2(0, 1), Adjacents.UP.vec),
                           (True,  Vec2(0, 1), Adjacents.DOWN.vec),
                           (False, Vec2(1, 0), Adjacents.LEFT.vec),
                           (False, Vec2(1, 0), Adjacents.RIGHT.vec)):
        oob = []
        for plot in region:
            adj = plot + step
            if adj not in region:
                oob.append(adj)
        if rev:
            oob.sort(key=lambda v: (v.y, v.x))
        else:
            oob.sort()

        unit = Vec2(vec.y, vec.x)
        for i in range(len(oob) - 1):
            a = oob[i]
            b = oob[i + 1]
            if a * vec != b * vec or abs(a - b) != unit:
                count += 1
        count += 1
    return count

def main():
    G = parse(fileinput.input())
    regions = garden_regions(G)
    r = sum(map(prod, zip(map(sides, regions), map(len, regions))))
    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit
