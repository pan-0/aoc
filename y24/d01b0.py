# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

import fileinput

Left = list[int]
Right = dict[int, int]

def parse(itr) -> tuple[Left, Right]:
    pairs = map(lambda line: map(int, line.strip().split("   ")), itr)
    L = []
    R = {}
    for x, y in pairs:
        L.append(x)
        R[y] = R.get(y, 0) + 1
    return (L, R)

def f(L: Left, R: Right) -> int:
    return sum(map(lambda x: x * R.get(x, 0), L))

def main():
    L, R = parse(fileinput.input())
    r = f(L, R)
    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit
