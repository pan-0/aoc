# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

import fileinput
import re
from itertools import chain
from math import prod

def parse(itr):
    num = r"([1-9][0-9]{0,2})"
    pat = fr"mul\({num},{num}\)"
    return chain.from_iterable(map(lambda line: re.finditer(pat, line), itr))

def main():
    pairs = parse(fileinput.input())
    r = sum(map(lambda pair: prod(map(int, pair.groups())), pairs))
    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit

