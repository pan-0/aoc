# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

import fileinput
from operator import add

def f(s: str) -> int:
    cords = [(0, 0), (0, 0)]
    grid = {cords[0]: 2}
    for i, move in enumerate(s):
        offset = {
            '^': ( 0, -1),
            'v': ( 0, +1),
            '>': (+1,  0),
            '<': (-1,  0)
        }[move]
        turn = i & 1
        loc = cords[turn] = (*map(add, cords[turn], offset),)
        grid[loc] = grid.get(loc, 0) + 1

    return len(grid)

def main():
    s = input()
    r = f(s)
    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit