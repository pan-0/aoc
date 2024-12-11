# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

import fileinput
from array import array
from functools import partial
from itertools import chain, islice, repeat, zip_longest
from math import prod

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

Sizes = array

def parse(itr) -> tuple[Sizes, Sizes]:
    nums = chain.from_iterable(map(lambda line: map(int, line.strip()), itr))
    files, spaces = map(partial(array, 'h'),
                        zip_longest(*batched(nums, 2), fillvalue=0))
    return (files, spaces)

def expand(files: Sizes, spaces: Sizes):
    layout = array('h')
    for i, (file, space) in enumerate(zip(files, spaces)):
        layout.extend(chain(repeat(i, file), repeat(-1 - i, space)))
    return layout

def first(itr, key=lambda x: True):
    return next(chain(filter(key, itr), (None,)))

def defrag(layout: Sizes, max_id: int):
    end = len(layout)
    prev_id = max_id + 1
    while (file_end := first(range(end, 0, -1),
                             key=lambda i: layout[i - 1] >= 0)) is not None:
        file_id = layout[file_end - 1]
        file_beg = first(range(file_end, -1, -1),
                         key=lambda i: layout[i - 1] != file_id)
        if file_id < prev_id:
            file_len = file_end - file_beg
            start = 0
            while (space_beg := first(range(start, len(layout)),
                                      key=lambda i: layout[i] < 0)) \
                    is not None and space_beg < file_beg:
                space_id = layout[space_beg]
                space_end = first(range(space_beg + 1, len(layout)),
                                  key=lambda i: layout[i] != space_id) \
                            or len(layout)
                space_len = space_end - space_beg
                if space_len >= file_len:
                    for i in range(file_len):
                        layout[space_beg + i] = file_id
                        layout[file_beg + i] = space_id
                    break
                start = space_end
            prev_id = file_id

        end = file_beg

def checksum(layout: Sizes) -> int:
    return sum(map(prod, enumerate(map(partial(max, 0), layout))))

def main():
    files, spaces = parse(fileinput.input())
    layout = expand(files, spaces)
    defrag(layout, len(files) - 1)
    r = checksum(layout)
    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit
