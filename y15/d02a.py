# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

import fileinput
from itertools import starmap

def parse(s: str):
    return map(int, s.split('x'))

def area(l: int, w: int, h: int) -> int:
    areas = (l * w, w * h, h * l)
    return 2 * sum(areas) + min(areas)

def main():
    r = sum(starmap(area, map(parse, fileinput.input())))
    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit