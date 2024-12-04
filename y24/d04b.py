# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

from __future__ import annotations

import fileinput
from pprint import pprint

Mat = list[str]

def parse(itr) -> Mat:
    return [*map(str.strip, itr)]

def is_mas(s: str) -> bool:
    return s in {"MAS", "SAM"}

def diag(M: Mat, i: int, j: int, sign: int) -> str:
    return "".join(map(lambda offs: M[i + offs][j + sign * offs], range(3)))

def f(M: Mat) -> int:
    digs = 0
    for i in range(len(M) - 2):
        for j in range(len(M[i]) - 2):
            diags = map(lambda offs, sign: diag(M, i, j + offs, sign),
                        (0, 2),
                        (1, -1))
            if all(map(is_mas, diags)):
                digs += 1
    return digs

def main():
    M = parse(fileinput.input())
    r = f(M)
    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit

