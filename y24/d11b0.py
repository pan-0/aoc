# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

import fileinput
from collections import defaultdict

Stones = dict[int, int]

def parse(itr) -> Stones:
    stones = defaultdict(int)
    inp = map(int, next(itr).strip().split(' '))
    for stone in inp:
        stones[stone] += 1
    return stones

def f(stones: Stones) -> int:
    for _ in range(75):
        next_stones = defaultdict(int)
        for stone, count in stones.items():
            if stone == 0:
                next_stones[1] += count
            elif (digits := len(str(stone))) & 1 == 0:
                q, r = divmod(stone, 10 ** (digits >> 1))
                next_stones[q] += count
                next_stones[r] += count
            else:
                next_stones[stone * 2024] += count
        stones = next_stones
    return sum(stones.values())

def main():
    stones = parse(fileinput.input())
    r = f(stones)
    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit