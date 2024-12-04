# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

import fileinput
from dataclasses import dataclass
from enum import Enum, auto

@dataclass(frozen=True)
class Point:
    x: int
    y: int

class Lights:
    def __init__(self, rows: int, cols: int):
        self.cols = cols
        self.vals = [0] * (rows * cols)

    def increase(self, begin: Point, end: Point, amount: int):
        vals, cols = self.vals, self.cols
        for i in range(begin.x, end.x + 1):
            for j in range(begin.y, end.y + 1):
                vals[i * cols + j] += amount

    def on(self, begin: Point, end: Point):
        self.increase(begin, end, 1)

    def off(self, begin: Point, end: Point):
        vals, cols = self.vals, self.cols
        for i in range(begin.x, end.x + 1):
            for j in range(begin.y, end.y + 1):
                idx = i * cols + j
                if vals[idx] > 0:
                    vals[idx] -= 1

    def toggle(self, begin: Point, end: Point):
        self.increase(begin, end, 2)

    def count(self) -> int:
        return sum(self.vals)

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
            lights.on(inst.begin, inst.end)
        elif inst.kind == InstKind.OFF:
            lights.off(inst.begin, inst.end)
        else:
            assert inst.kind == InstKind.TOGGLE
            lights.toggle(inst.begin, inst.end)

    r = lights.count()
    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit