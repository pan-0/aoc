# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

from __future__ import annotations

import fileinput
from pprint import pprint

Mat = list[str]

def parse(itr) -> Mat:
    return [*map(str.strip, itr)]

def xmas_n(s: str) -> int:
    return sum(map(s.count, ("XMAS", "SAMX")))

def dim(itr) -> int:
    return sum(map(xmas_n, itr))

def diag(M: Mat, i: int, j: int, sign: int) -> str:
    return "".join(map(lambda offs: M[i + offs][j + sign * offs], range(4)))

def f(M: Mat) -> int:
    rows = dim(M)
    cols = dim(map("".join, zip(*M)))
    digs = 0
    for i in range(0, len(M) - 3):
        for begin, sign in (0, 1), (3, -1):
            for j in range(begin, begin + len(M[i]) - 3):
                digs += xmas_n(diag(M, i, j, sign))
    return rows + cols + digs

def main():
    M = parse(fileinput.input())
    r = f(M)
    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit

