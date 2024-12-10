# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

import fileinput
from collections import defaultdict
from string import digits

Grid = list[str]

def parse(itr) -> Grid:
    return [*map(str.strip, itr)]

def f(G: Grid) -> tuple[int, int]:
    rows = len(G)
    cols = len(G[0])
    trailheads = defaultdict(int)
    for i in range(rows):
        for j in range(cols):
            stack = [(0, i, j)]
            while stack:
                c, x, y = stack.pop()
                if 0 <= x < rows and 0 <= y < cols and G[x][y] == digits[c]:
                    if digits[c] == digits[-1]:
                        trailheads[i, j, x, y] += 1
                    else:
                        stack.extend(((c + 1, x - 1, y),
                                      (c + 1, x + 1, y),
                                      (c + 1, x, y - 1),
                                      (c + 1, x, y + 1),))
    return (len(trailheads), sum(trailheads.values()))

def main():
    G = parse(fileinput.input())
    ra, rb = f(G)
    print(ra, rb)

if __name__ == "__main__":
    main()
    raise SystemExit
