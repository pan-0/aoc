# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

import fileinput
from itertools import chain, islice, zip_longest

def batched(itr, n, *, strict=False):
    # batched('ABCDEFG', 3) → ABC DEF G
    if n < 1:
        raise ValueError("n must be at least one")
    it = iter(itr)
    while batch := (*islice(it, n),):
        if strict and len(batch) != n:
            raise ValueError("batched(): incomplete batch")
        yield batch

Sizes = tuple[int, ...]

def parse(itr) -> tuple[Sizes, Sizes]:
    nums = chain.from_iterable(map(lambda line: map(int, line.strip()), itr))
    sizes, empty = zip_longest(*batched(nums, 2), fillvalue=0)
    return (sizes, empty)

Diskmap = list[tuple[int, int]]

def compact(sizes: Sizes, empty: Sizes) -> Diskmap:
    end = len(sizes) - 1
    filled = 0
    r = []
    i = 0
    while i < end:
        r.append((sizes[i], i))
        empty_block = empty[i]
        while empty_block > 0 and end > i:
            last = sizes[end] - filled
            fit = min(last, empty_block)
            r.append((fit, end))
            empty_block -= last
            if empty_block >= 0:
                end -= 1
                filled = 0
            else:
                filled += fit
        i += 1
    r.append((sizes[i] - filled, i))
    return r

def checksum(diskmap: Diskmap) -> int:
    r = 0
    offset = 0
    for length, idn in diskmap:
        r += sum(map(lambda pos: (pos + offset) * idn, range(length)))
        offset += length
    return r

def main():
    sizes, empty = parse(fileinput.input())
    compacted = compact(sizes, empty)
    r = checksum(compacted)
    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit
