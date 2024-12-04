# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

import fileinput
from bisect import bisect_right
from itertools import takewhile
from functools import cache

class Buckets(list[int]):
    def __hash__(self) -> int:
        return id(self)

def parse(itr) -> Buckets:
    return Buckets(sorted(map(int, itr)))

@cache
def crunch(buckets: Buckets, index: int, alloted: int) -> int:
    if alloted == 0:
        return 1

    end = bisect_right(buckets, alloted, lo=index)
    return sum(map(lambda i: crunch(buckets, i + 1, alloted - buckets[i]),
                   range(index, end)))

def solve(buckets: Buckets, n: int) -> int:
    return crunch(buckets, 0, n)

def main():
    buckets = parse(fileinput.input())
    r = solve(buckets, 150)
    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit