# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

import fileinput
from concurrent.futures import ProcessPoolExecutor as Pool
from itertools import product
from functools import partial
from operator import add, mul

System = tuple[int, list[int]]
Input = list[System]

def parse(s: str) -> System:
    x, nums = s.split(':')
    return (int(x), [*map(int, nums.strip().split(' '))])

def cat(l: int, r: int) -> int:
    return int(str(l) + str(r))

def solve_equation(x: int, nums: list[int], ops) -> int:
    for prod in product(ops, repeat=len(nums) - 1):
        l = nums[0]
        for i, op in enumerate(prod, start=1):
            l = op(l, nums[i])
            if l > x:
                break
        else:
            if l == x:
                return x
    return 0

def solve_system(ops, system: System) -> int:
    return solve_equation(system[0], system[1], ops)

def solve(inp: Input, ops) -> int:
    with Pool() as pool:
        return sum(pool.map(partial(solve_system, ops), inp))

def main():
    inp = [*map(parse, fileinput.input())]
    ra = solve(inp, (add, mul))
    rb = solve(inp, (add, mul, cat))
    print(ra, rb)

if __name__ == "__main__":
    main()
    raise SystemExit
