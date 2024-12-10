# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

import fileinput
from itertools import chain, islice, zip_longest

try:
    from itertools import batched
except ImportError:
    def batched(itr, n, *, strict=False):
        # batched("ABCDEFG", 3) -> ABC DEF G
        if n < 1:
            raise ValueError("n must be at least one")
        it = iter(itr)
        while batch := (*islice(it, n),):
            if strict and len(batch) != n:
                raise ValueError("batched(): incomplete batch")
            yield batch

Sizes = bytes

def parse(itr) -> tuple[Sizes, Sizes]:
    nums = chain.from_iterable(map(lambda line: map(int, line.strip()), itr))
    files, spaces = map(bytes, zip_longest(*batched(nums, 2), fillvalue=0))
    return (files, spaces)

def compact(files: Sizes, spaces: Sizes):
    end = len(files) - 1
    filled = 0
    i = 0
    while i < end:
        yield (files[i], i)
        space = spaces[i]
        while space > 0 and end > i:
            last = files[end] - filled
            fit = min(last, space)
            yield (fit, end)
            space -= last
            if space >= 0:
                end -= 1
                filled = 0
            else:
                filled += fit
        i += 1
    yield (files[i] - filled, i)

def checksum(diskmap) -> int:
    r = 0
    offset = 0
    for length, idn in diskmap:
        r += sum(map(lambda pos: (pos + offset) * idn, range(length)))
        offset += length
    return r

def main():
    files, spaces = parse(fileinput.input())
    compacted = compact(files, spaces)
    r = checksum(compacted)
    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit
