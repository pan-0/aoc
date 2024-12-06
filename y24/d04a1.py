# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

import fileinput

Grid = list[str]

def parse(itr) -> Grid:
    return [*map(str.strip, itr)]

def xmas_n(s: str) -> int:
    return sum(map(s.count, ("XMAS", "SAMX")))

def count(itr) -> int:
    return sum(map(xmas_n, itr))

def diag(G: Grid, i: int, j: int, sign: int) -> str:
    return "".join(map(lambda offs: G[i + offs][j + sign * offs], range(4)))

def f(G: Grid) -> int:
    rows = count(G)
    cols = count(map("".join, zip(*G)))
    digs = 0
    for i in range(len(G) - 3):
        for j in range(len(G[i]) - 3):
            diags = map(lambda offs, sign: diag(G, i, j + offs, sign),
                        (0, 3),
                        (1, -1))
            digs += count(diags)
    return rows + cols + digs

def main():
    G = parse(fileinput.input())
    r = f(G)
    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit
