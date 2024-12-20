# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

import fileinput
from typing import NamedTuple

class Equ(NamedTuple):
    lhs: int
    rhs: list[int]

def parse(s: str) -> Equ:
    r, nums = s.split(':')
    return Equ(int(r), [*map(int, nums.strip().split(' '))])

def is_sat(lhs: int, rhs: list[int], length: int) -> bool:
    end = length - 1
    last = rhs[end]
    if end == 0:
        return lhs == last

    if lhs < last:
        return False

    q, r = divmod(lhs, last)
    return (r == 0 and is_sat(q, rhs, end)) or is_sat(lhs - last, rhs, end)

def main():
    inp = map(parse, fileinput.input())
    r = sum(map(lambda equ: equ.lhs,
                filter(lambda equ: is_sat(*equ, len(equ.rhs)), inp)))
    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit
