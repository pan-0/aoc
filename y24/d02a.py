# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

import fileinput
from itertools import chain

def parse(itr):
    return map(lambda line: map(int, line.strip().split(" ")), itr)

def sign(x: int) -> int:
    return 1 if x >= 0 else -1

def is_safe(report, diff_min: int=1, diff_max: int=3) -> bool:
    q = next(report)
    p = next(report)
    sgn = sign(q - p)
    for level in chain((p,), report):
        diff = q - level
        if sign(diff) != sgn or not (diff_min <= abs(diff) <= diff_max):
            return False

        q = level
    return True

def main():
    r = sum(map(is_safe, parse(fileinput.input())))
    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit
