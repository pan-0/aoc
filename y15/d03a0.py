# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

import fileinput
from operator import add

def f(s: str) -> int:
    cords = (0, 0)  # x, y
    grid = {cords: 1}
    for move in s:
        offset = {
            '^': ( 0, -1),
            'v': ( 0, +1),
            '>': (+1,  0),
            '<': (-1,  0)
        }[move]
        cords = (*map(add, cords, offset),)
        grid[cords] = grid.get(cords, 0) + 1

    return len(grid)

def main():
    s = input()
    r = f(s)
    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit