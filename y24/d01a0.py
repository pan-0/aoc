# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

import fileinput
import heapq

List = list[int]

def parse(itr) -> tuple[List, List]:
    pairs = map(lambda line: map(int, line.strip().split("   ")), itr)
    A = []
    B = []
    for x, y in pairs:
        heapq.heappush(A, x)
        heapq.heappush(B, y)
    return (A, B)

def f(A: List, B: List) -> int:
    dist = 0
    while A and B:
        dist += abs(heapq.heappop(A) - heapq.heappop(B))
    return dist

def main():
    A, B = parse(fileinput.input())
    r = f(A, B)
    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit
