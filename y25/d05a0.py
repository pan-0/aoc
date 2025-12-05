# {{{
# Copyright (C) 2025 by pan <pan_@disroot.org>
# SPDX-License-Identifier: 0BSD

# vi: foldmethod=marker
from __future__ import annotations
from prelude import *
# }}}

def parse(itr: Iterator[str]) -> tuple[list[int, int], Iterator[int]]:
    return ([*map(lambda rng: (*map(int, rng.split('-')),),
                  takewhile(lambda line: line != "", itr))],
            map(int, itr))

def go(inp: Input) -> Iterator[int]:
    ranges, ids = parse(inp)
    count = 0
    for iid in ids:
        count += any(a <= iid <= b for a, b in ranges)
    yield count

# {{{
if __name__ == "__main__":
    utils.main(go)
    sys.exit()
# }}}
