# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

import fileinput
from dataclasses import dataclass
from enum import Enum, auto

POPCOUNT = (*map(lambda x: bin(x).count('1'), range(256)),)

def ceildiv(x: int, y: int) -> int:
    assert x > 0
    return 1 + (x - 1) // y

@dataclass(frozen=True)
class Point:
    x: int
    y: int

class Lights:
    WIDTH = 8
    MAX = (1 << (WIDTH - 1)) | ((1 << (WIDTH - 1)) - 1)
    MASK = WIDTH - 1
    SHIFT = WIDTH.bit_length() - 1

    def __init__(self, rows: int, cols: int):
        self.cols = cols
        self.bits = bytearray((0,)) * ceildiv(rows * cols, self.WIDTH)

    def set(self, row: int, col: int, bit: bool):
        idx = row * self.cols + col
        unit = idx >> self.SHIFT
        shift = idx & self.MASK
        self.bits[unit] = (self.bits[unit] & (self.MAX ^ (1 << shift))) \
                          | (bit << shift)

    def flip(self, row: int, col: int):
        idx = row * self.cols + col
        self.bits[idx >> self.SHIFT] ^= 1 << (idx & self.MASK)

    def onoff(self, begin: Point, end: Point, on: bool):
        for i in range(begin.x, end.x + 1):
            for j in range(begin.y, end.y + 1):
                self.set(i, j, on)

    def toggle(self, begin: Point, end: Point):
        for i in range(begin.x, end.x + 1):
            for j in range(begin.y, end.y + 1):
                self.flip(i, j)

    def count(self) -> int:
        #return sum(map(int.bit_count, self.bits))
        return sum(map(lambda x: POPCOUNT[x], self.bits))

class InstKind(Enum):
    ON = auto()
    TOGGLE = auto()
    OFF = auto()

@dataclass(frozen=True)
class Inst:
    kind: InstKind
    begin: Point
    end: Point

def points(s: list[str]) -> tuple[Point, Point]:
    x0, y0 = map(int, s[0].split(','))
    x1, y1 = map(int, s[2].split(','))
    return (Point(x0, y0), Point(x1, y1))

def parse(s: str) -> Inst:
    parts = s.split(' ')
    begin, end = points(parts[1 + (parts[0] == "turn"):])
    return Inst(
        (InstKind.TOGGLE if parts[0] == "toggle" else
         InstKind.ON     if parts[1] == "on"     else
         InstKind.OFF   #if parts[1] == "off"    else None  # WTF
        ),
        begin,
        end
    )

def main():
    lights = Lights(1000, 1000)
    for inst in map(parse, fileinput.input()):
        if inst.kind == InstKind.ON:
            lights.onoff(inst.begin, inst.end, True)
        elif inst.kind == InstKind.OFF:
            lights.onoff(inst.begin, inst.end, False)
        else:
            assert inst.kind == InstKind.TOGGLE
            lights.toggle(inst.begin, inst.end)

    r = lights.count()
    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit