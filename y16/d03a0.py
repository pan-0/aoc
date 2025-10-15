# Copyright (C) 2025 by pan <pan_@disroot.org>
# SPDX-License-Identifier: 0BSD

import fileinput
import utils

from itertools import combinations
from typing import Iterator

def parse(itr: Iterator[str]) -> Iterator[tuple[int, int, int]]:
    return utils.batched(utils.integers(itr), 3)

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
