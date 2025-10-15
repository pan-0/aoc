# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

from __future__ import annotations

import fileinput
import utils

from collections import defaultdict
from itertools import takewhile
from math import prod

Grid = utils.Grid[str]
Vec2 = utils.Vec2[int]

def parse(itr) -> Grid:
    return Grid([*map(str.strip, takewhile(lambda line: line != "\n", itr))])

Regions = list[list[Vec2]]

def garden_regions(G: Grid) -> Regions:
    regions = []
    found = set()
    for i in range(G.rows):
        for j in range(G.cols):
            orig = Vec2(j, i)
            plant = G[orig]

            region = []
            for plot in G.dfs(orig,
                              key=lambda x: x not in found and G[x] == plant,
                              adj=G.adjacent_cross):
                found.add(plot)
                region.append(plot)

            if region:
                regions.append(region)

    return regions

def perim(region: list[Vec2]) -> int:
    adj = 0
    for plot in region:
        adj += sum(map(lambda offs: plot + offs in region,
                       Grid.ADJACENT_CROSS))
    return 4 * len(region) - adj

def main():
    G = parse(fileinput.input())
    regions = garden_regions(G)
    r = sum(map(prod, zip(map(perim, regions), map(len, regions))))
    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit
