# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

import fileinput
import utils
from enum import Enum
from functools import partial
from itertools import chain, takewhile
from typing import Iterator, Optional
from utils import Adjacents

class Cell(Enum):
    WALL  = '#'
    EMPTY = '.'
    BOX_L = '['
    BOX_R = ']'
    ROBOT = '@'

    def __str__(self) -> str:
        return self.value

Vec2 = utils.Vec2[int]
Grid = utils.MutGrid[Cell]

def cell(c: str) -> tuple[Cell, Cell]:
    return {'#': (Cell.WALL,  Cell.WALL),  '.': (Cell.EMPTY, Cell.EMPTY),
            'O': (Cell.BOX_L, Cell.BOX_R), '@': (Cell.ROBOT, Cell.EMPTY)}[c]

def move(c: str) -> Adjacents:
    return {'^': Adjacents.UP,   'v': Adjacents.DOWN,
            '<': Adjacents.LEFT, '>': Adjacents.RIGHT}[c]

def parse(itr) -> tuple[Grid, Iterator[Adjacents]]:
    G = Grid([*map(lambda row: [*chain.from_iterable(map(cell, row.strip()))],
                   takewhile(lambda line: line != "\n", itr))])
    return (G, map(move, chain.from_iterable(map(str.strip, itr))))

def horizontal_end(G: Grid, pos: Vec2, vec: Vec2) -> Vec2:
    end = pos + vec
    while G[end] in {Cell.BOX_L, Cell.BOX_R}:
        end += vec
    return end if G[end] == Cell.EMPTY else pos

def box_left(G: Grid, box: Vec2) -> Vec2:
    return box + {Cell.BOX_L: Vec2(0, 0),
                  Cell.BOX_R: Adjacents.LEFT.vec}[G[box]]

def box_other(G: Grid, box: Vec2) -> Vec2:
    return box + {Cell.BOX_L: Adjacents.RIGHT,
                  Cell.BOX_R: Adjacents.LEFT}[G[box]].vec

def has_space(G: Grid, vec: Vec2, box_l: Vec2) -> bool:
    box_r = box_l + Adjacents.RIGHT.vec
    return G[box_l + vec] != Cell.WALL and G[box_r + vec] != Cell.WALL

def vertical_moves(G: Grid, pos: Vec2, vec: Vec2) -> Optional[set[Vec2]]:
    end = pos + vec
    if G[end] == Cell.WALL:
        return None

    if G[end] == Cell.EMPTY:
        return {}

    boxes = {*map(partial(box_left, G),
                  G.dfs(end,
                        key=lambda v: G[v] in {Cell.BOX_L, Cell.BOX_R},
                        adj=lambda box: (box + vec, box_other(G, box) + vec)))}
    return boxes if all(map(partial(has_space, G, vec), boxes)) else None

def walk(G: Grid, robot: Vec2, moves: Iterator[Adjacents]):
    for move in moves:
        vec = move.vec
        if move in {Adjacents.UP, Adjacents.DOWN}:
            boxes = vertical_moves(G, robot, vec)
            if boxes is not None:
                for box_l in boxes:
                    box_r = box_l + Adjacents.RIGHT.vec
                    G[box_l] = G[box_r] = Cell.EMPTY

                for box_l in boxes:
                    box_r = box_l + Adjacents.RIGHT.vec
                    G[box_l + vec] = Cell.BOX_L
                    G[box_r + vec] = Cell.BOX_R

                G[robot] = Cell.EMPTY
                robot += vec
                G[robot] = Cell.ROBOT
        elif (it := horizontal_end(G, robot, vec)) != robot:
            while True:
                prev = it - vec
                G[it] = G[prev]
                G[prev] = Cell.EMPTY
                it = prev
                if it == robot:
                    break
            robot += vec

def box_cords(G: Grid) -> Iterator[int]:
    for i in range(1, G.rows - 1):
        for j in range(2, G.cols - 2, 2):
            val = {Cell.BOX_L: 0, Cell.BOX_R: 1}.get(G[i, j])
            if val is not None:
                yield 100 * i + j - val

def main():
    G, moves = parse(fileinput.input())
    robot = G.find(Cell.ROBOT)
    walk(G, robot, moves)
    r = sum(box_cords(G))
    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit
