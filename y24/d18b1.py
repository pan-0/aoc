# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

import fileinput
import utils
from typing import Iterator, Optional

Grid = utils.MutGrid[str]
Vec2 = utils.Vec2[int]
Bytes = Iterator[Vec2]

def parse(itr) -> Bytes:
    return map(lambda line: Vec2(*map(int, line.strip().split(','))), itr)

def build_grid(bytez: Bytes) -> Grid:
    grid = Grid.empty(71, 71, '.')
    for byte in utils.take(bytez, 1024):
        grid[byte] = '#'
    return grid

def path_exists(grid: Grid, S: Vec2, E: Vec2) -> bool:
    for tile in grid.dfs(E,
                         key=lambda v: grid[v] != '#',
                         adj=grid.adjacent_cross):
        if tile == S:
            return True
    return False

def first_byte(grid: Grid, bytez_: Bytes, S: Vec2, E: Vec2) -> Vec2:
    bytez = [*bytez_]
    left = 0
    right = len(bytez) - 1
    mid = 0
    while left < right:
        mid = (left + right) // 2
        for bef in range(mid + 1):
            grid[bytez[bef]] = '#'
        for aft in range(mid + 2, len(bytez)):
            grid[bytez[aft]] = '.'
        if path_exists(grid, S, E):
            left = mid + 1
        else:
            right = mid - 1
    return bytez[mid + 1]

def main():
    bytez = parse(fileinput.input())
    grid = build_grid(bytez)
    S = Vec2(0, 0)
    E = Vec2(grid.cols - 1, grid.rows - 1)
    byte = first_byte(grid, bytez, S, E)
    r = ",".join(map(str, byte))
    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit
