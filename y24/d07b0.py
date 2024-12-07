# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

import fileinput
from itertools import product
from operator import add, mul

def parse(s: str):
    r, nums = s.split(':')
    return (int(r), map(int, nums.strip().split(' ')))

def cat(l: int, r: int) -> int:
    return int(str(l) + str(r))

def main():
    inp = map(parse, fileinput.input())
    c = 0
    for r, nums in inp:
        lst = [*nums]
        for ops in product((add, mul, cat), repeat=len(lst) - 1):
            l = lst[0]
            for i, op in enumerate(ops, start=1):
                l = op(l, lst[i])
            if l == r:
                c += r
                break
    print(c)

if __name__ == "__main__":
    main()
    raise SystemExit
