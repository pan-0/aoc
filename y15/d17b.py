# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

import fileinput
from itertools import dropwhile, takewhile

def parse(itr) -> list[int]:
    return sorted(map(int, itr), reverse=True)

def crunch(buckets: list[int], index: int, alloted: int, used: int) -> list:
    if alloted == 0:
        yield used
    else:
        indices = dropwhile(lambda i: buckets[i] > alloted,
                            range(index, len(buckets)))
        for i in takewhile(lambda i: buckets[i] <= alloted, indices):
            yield from crunch(buckets, i + 1, alloted - buckets[i], used + 1)

def solve(buckets: list, n: int) -> int:
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