# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

import fileinput
from bisect import bisect_right
from functools import cache

class Buckets(list[int]):
    def __hash__(self) -> int:
        return id(self)

def parse(itr) -> Buckets:
    return Buckets(sorted(map(int, itr)))

@cache
def find_end(buckets: Buckets, index: int, alloted: int) -> int:
    return bisect_right(buckets, alloted, lo=index)

def crunch(buckets: Buckets, index: int, alloted: int, used: int):
    if alloted == 0:
        yield used
    else:
        end = find_end(buckets, index, alloted)
        for i in range(index, end):
            yield from crunch(buckets, i + 1, alloted - buckets[i], used + 1)

def solve(buckets: Buckets, n: int) -> int:
    combs = crunch(buckets, 0, n, 0)
    best = next(combs)
    count = 1
    for length in combs:
        if length < best:
            best = length
            count = 1
        elif length == best:
            count += 1
    return count

def main():
    buckets = parse(fileinput.input())
    r = solve(buckets, 150)
    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit