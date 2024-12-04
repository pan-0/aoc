# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

import fileinput
from itertools import starmap

def parse(s: str):
    return map(int, s.split('x'))

def ribbon(l: int, w: int, h: int) -> int:
    faces = (l + w, w + h, h + l)
    return 2 * min(faces) + l * w * h

def main():
    r = sum(starmap(ribbon, map(parse, fileinput.input())))
    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit