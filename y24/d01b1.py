# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

import fileinput
from collections import Counter

def parse(itr):
    return map(lambda line: map(int, line.strip().split("   ")), itr)

def main():
    L = []
    R = Counter()
    for x, y in parse(fileinput.input()):
        L.append(x)
        R[y] += 1
    r = sum(map(lambda x: x * R.get(x, 0), L))
    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit
