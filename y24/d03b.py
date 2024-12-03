# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

import fileinput
import re
from itertools import chain, islice
from math import prod

def parse(itr):
    num = r"([1-9][0-9]{0,2})"
    pat = fr"mul\({num},{num}\)|(don't\(\))|(do\(\))"
    return chain.from_iterable(map(lambda line: re.finditer(pat, line), itr))

def f(stmts) -> int:
    acc = 0
    do = True
    for stmt in stmts:
        match stmt.lastindex:
            case 2:
                if do:
                    acc += prod(map(int, islice(stmt.groups(), 2)))
            case 3:
                do = False
            case 4:
                do = True
    return acc

def main():
    stmts = parse(fileinput.input())
    r = f(stmts)
    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit

