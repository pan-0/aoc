# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

import fileinput
from typing import NamedTuple
from operator import mul
from math import prod

class Ingredient(NamedTuple):
    capacity: int
    durability: int
    flavor: int
    texture: int
    calories: int

def parse(s: str) -> Ingredient:
    parts = s.split(' ')
    return Ingredient(*map(lambda i: int(parts[i][:-1]), (2, 4, 6, 8, 10)))

def propsum(teaspoons: list[int], props) -> int:
    return max(sum(map(mul, teaspoons, props)), 0)

def score(teaspoons: list[int], ingredients: list[Ingredient]) -> int:
    return prod(map(lambda i: propsum(teaspoons, map(lambda ingred: ingred[i],
                                                     ingredients)),
                    range(4)))

def crunch(ingredients: list[Ingredient],
           alloted: int,
           teaspoons: list[int],
           index: int,
           best: int=0) -> int:
    if index >= len(teaspoons):
        return max(score(teaspoons, ingredients), best)

    for n in range(alloted + 1):
        temp = teaspoons.copy()
        temp[index] = n
        best = crunch(ingredients, alloted - n, temp, index + 1, best)

    return best

def solve(ingredients: list[Ingredient], n: int) -> int:
    return crunch(ingredients, n, [0] * len(ingredients), 0)

def main():
    ingredients = [*map(parse, fileinput.input())]
    r = solve(ingredients, 100)
    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit