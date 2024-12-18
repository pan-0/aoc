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
    for byte in utils.take(bytez, 1024 - 1):
        grid[byte] = '#'
    return grid

def first_byte(grid: Grid, bytez: Bytes, S: Vec2, E: Vec2) -> Optional[Vec2]:
    for byte in bytez:
        grid[byte] = '#'
        for tile in grid.dfs(E,
                             key=lambda v: grid[v] != '#',
                             adj=grid.adjacent_cross):
            if tile == S:
                break
        else:
            return byte
    return None

def main():
    bytez = parse(fileinput.input())
    grid = build_grid(bytez)
    S = Vec2(0, 0)
    E = Vec2(grid.cols - 1, grid.rows - 1)
    byte = first_byte(grid, bytez, S, E)
    if byte is not None:
        r = ",".join(map(str, byte))
        print(r)

if __name__ == "__main__":
    main()
    raise SystemExit
