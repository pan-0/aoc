# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

import fileinput

Stones = list[int]

def parse(itr) -> Stones:
    return [*map(int, next(itr).strip().split(' '))]

def f(stones: Stones) -> int:
    for _ in range(25):
        for i in range(len(stones)):
            stone = stones[i]
            if stone == 0:
                stones[i] = 1
            elif (digits := len(str(stone))) & 1 == 0:
                q, r = divmod(stone, 10 ** (digits >> 1))
                stones[i] = q
                stones.append(r)
            else:
                stones[i] *= 2024
    return len(stones)

def main():
    stones = parse(fileinput.input())
    r = f(stones)
    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit
