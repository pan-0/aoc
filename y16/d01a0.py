# Copyright (C) 2025 by pan <pan_@disroot.org>
# SPDX-License-Identifier: 0BSD

import fileinput
import utils

from enum import Enum, auto
from dataclasses import dataclass
from typing import Iterator
from utils import Adjacents

Vec2 = utils.Vec2[int]

class Turn(Enum):
    LEFT  = auto()
    RIGHT = auto()

@dataclass(frozen=True)
class Instruction:
    turn: Turn
    blocks: int

class Orientation(Enum):
    NORTH = auto()
    EAST  = auto()
    SOUTH = auto()
    WEST  = auto()

def parse(itr: Iterator[str]) -> Iterator[Instruction]:
    line = next(itr)
    return map(lambda inst: \
                Instruction({'L': Turn.LEFT, 'R': Turn.RIGHT}[inst[0]],
                            int(inst[1:])),
               line.split(", "))

TURN_TABLE: dict[tuple[Orientation, Turn], Orientation] = {
    (Orientation.NORTH, Turn.LEFT):  Orientation.WEST,
    (Orientation.NORTH, Turn.RIGHT): Orientation.EAST,
    (Orientation.EAST,  Turn.LEFT):  Orientation.NORTH,
    (Orientation.EAST,  Turn.RIGHT): Orientation.SOUTH,
    (Orientation.SOUTH, Turn.LEFT):  Orientation.EAST,
    (Orientation.SOUTH, Turn.RIGHT): Orientation.WEST,
    (Orientation.WEST,  Turn.LEFT):  Orientation.SOUTH,
    (Orientation.WEST,  Turn.RIGHT): Orientation.NORTH
}

STEP_VEC: dict[Orientation, Vec2] = {
    Orientation.NORTH: Adjacents.UP.vec,
    Orientation.EAST:  Adjacents.RIGHT.vec,
    Orientation.SOUTH: Adjacents.DOWN.vec,
    Orientation.WEST:  Adjacents.LEFT.vec
}

def main():
    insts = parse(fileinput.input())
    ori = Orientation.NORTH
    pos = Vec2(0, 0)
    for inst in insts:
        ori = TURN_TABLE[ori, inst.turn]
        pos += STEP_VEC[ori] * inst.blocks

    r = sum(map(abs, pos))
    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit
