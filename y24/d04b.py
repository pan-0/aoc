# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

from __future__ import annotations

import fileinput

Grid = list[str]

def parse(itr) -> Grid:
    return [*map(str.strip, itr)]

def is_mas(s: str) -> bool:
    return s in {"MAS", "SAM"}

def diag(G: Grid, i: int, j: int, sign: int) -> str:
    return "".join(map(lambda offs: G[i + offs][j + sign * offs], range(3)))

def f(G: Grid) -> int:
    digs = 0
    for i in range(len(G) - 2):
        for j in range(len(G[i]) - 2):
            diags = map(lambda offs, sign: diag(G, i, j + offs, sign),
                        (0, 2),
                        (1, -1))
            if all(map(is_mas, diags)):
                digs += 1
    return digs

def main():
    G = parse(fileinput.input())
    r = f(G)
    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit

