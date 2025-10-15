# Copyright (C) 2025 by pan <pan_@disroot.org>
# SPDX-License-Identifier: 0BSD

import fileinput
import utils

from itertools import takewhile
from typing import Iterator
from utils import Adjacent, Adjacents

Grid = utils.Grid[str]

def parse(line: str) -> Iterator[Adjacent]:
    return map({'U': Adjacents.UP.value,
                'D': Adjacents.DOWN.value,
                'L': Adjacents.LEFT.value,
                'R': Adjacents.RIGHT.value}.get, line.strip())

def main():
    keypad = Grid(("  1  ",
                   " 234 ",
                   "56789",
                   " ABC ",
                   "  D  "))
    pos = keypad.find('5')
    buttons = []
    for line in takewhile(lambda line: line != "\n", fileinput.input()):
        for adj in parse(line):
            new_pos = pos + adj.vec
            if keypad.is_inbounds(new_pos) and keypad[new_pos] != ' ':
                pos = new_pos
        buttons.append(keypad[pos])

    r = "".join(buttons)
    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit
