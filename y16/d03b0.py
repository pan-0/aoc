# Copyright (C) 2025 by pan <pan_@disroot.org>
# SPDX-License-Identifier: 0BSD

import fileinput
import utils

from itertools import combinations
from typing import Iterator

def parse(itr: Iterator[str]) -> Iterator[list[int]]:
    nines = utils.batched(utils.integers(itr), 9)
    for nums in nines:
        triples = ([], [], [])
        for threes in utils.batched(nums, 3):
            for triple, num in zip(triples, threes):
                triple.append(num)
        yield from triples

def main():
    inp = parse(fileinput.input())
    combs = [*combinations(range(3), r=2)]
    valid = 0
    for nums in inp:
        for i, j in combs:
            k = 3 - i - j
            if nums[i] + nums[j] <= nums[k]:
                break
        else:
            valid += 1
    print(valid)

if __name__ == "__main__":
    main()
    raise SystemExit
