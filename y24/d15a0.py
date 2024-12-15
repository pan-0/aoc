# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

import fileinput
import utils
from enum import Enum
from itertools import chain, takewhile
from typing import Iterator
from utils import Adjacents

class Cell(Enum):
    WALL  = '#'
    EMPTY = '.'
    BOX   = 'O'
    ROBOT = '@'

    def __str__(self) -> str:
        return self.value

Vec2 = utils.Vec2[int]
Grid = utils.MutGrid[Cell]

def cell(c: str) -> Cell:
    return {'#': Cell.WALL, '.': Cell.EMPTY, 'O': Cell.BOX, '@': Cell.ROBOT}[c]

def move(c: str) -> Adjacents:
    return {'^': Adjacents.UP,   'v': Adjacents.DOWN,
            '<': Adjacents.LEFT, '>': Adjacents.RIGHT}[c]

def parse(itr) -> tuple[Grid, Iterator[Adjacents]]:
    G = Grid([*map(lambda row: [*map(cell, row.strip())],
                   takewhile(lambda line: line != "\n", itr))])
    return (G, map(move, chain.from_iterable(map(str.strip, itr))))

def move_end(G: Grid, pos: Vec2, vec: Vec2) -> Vec2:
    end = pos + vec
    while G[end] == Cell.BOX:
        end += vec
    return end if G[end] == Cell.EMPTY else pos

def walk(G: Grid, robot: Vec2, moves: Iterator[Adjacents]):
    for move in moves:
        vec = move.vec
        end = move_end(G, robot, vec)
        if end != robot:
            G[end] = Cell.BOX
            G[robot] = Cell.EMPTY
            robot += vec
            G[robot] = Cell.ROBOT

def box_cords(G: Grid) -> Iterator[int]:
    for i in range(1, G.rows - 1):
        for j in range(1, G.cols - 1):
            if G[i, j] == Cell.BOX:
                yield 100 * i + j

def main():
    G, moves = parse(fileinput.input())
    robot = G.find(Cell.ROBOT)
    walk(G, robot, moves)
    r = sum(box_cords(G))
    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit
