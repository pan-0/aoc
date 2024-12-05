# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

import fileinput
import string
from itertools import product

PAIRS = (*map("".join, product(string.ascii_lowercase, repeat=2)),)
TRIPLES = (*map(lambda p: p + p[0], PAIRS),)

def nice(s: str) -> bool:
    for pair in PAIRS:
        i = s.find(pair)
        if i >= 0 and s.find(pair, i + 2) >= 0:
            break
    else:
        return False

    return any(map(lambda t: t in s, TRIPLES))

def main():
    r = sum(map(nice, fileinput.input()))
    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit