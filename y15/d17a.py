# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

import fileinput
from itertools import dropwhile, takewhile

def parse(itr) -> list[int]:
    return sorted(map(int, itr), reverse=True)

def crunch(buckets: list[int], index: int, alloted: int) -> int:
    if alloted == 0:
        return 1

    # Could do a binary search since the `buckets` are sorted.
    indices = dropwhile(lambda i: buckets[i] > alloted,
                        range(index, len(buckets)))
    return sum(map(lambda i: crunch(buckets, i + 1, alloted - buckets[i]),
                   takewhile(lambda i: buckets[i] <= alloted, indices)))

def solve(buckets: list[int], n: int) -> int:
    return crunch(buckets, 0, n)

def main():
    buckets = parse(fileinput.input())
    r = solve(buckets, 150)
    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit