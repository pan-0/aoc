# {{{
# Copyright (C) 2025 by pan <pan_@disroot.org>
# SPDX-License-Identifier: 0BSD

# vi: foldmethod=marker
from __future__ import annotations
from prelude import *
# }}}

class Range(NamedTuple):
    a: int
    b: int

def parse(itr: Iterator[str]) -> Iterator[Range]:
    return map(lambda rng: Range(*map(int, rng.split('-')),),
               takewhile(lambda line: line != "", itr))

def union(X: Range, Y: Range) -> Optional[Range]:
    if X.a > Y.a:
        X, Y = Y, X
    return X if X.b >= Y.b else (Range(X.a, Y.b) if X.b >= Y.a else None)

def add_range(ranges: list[Range], R: Range):
    for i, Q in enumerate(ranges):
        U = union(Q, R)
        if U is not None:
            if U != Q:
                swap_pop(ranges, i)
                add_range(ranges, U)
            break
    else:
        ranges.append(R)

def go(inp: Input) -> Iterator[int]:
    ranges = []
    for R in parse(inp):
        add_range(ranges, R)
    res = sum(map(lambda R: R.b - R.a + 1, ranges))
    yield res

# {{{
if __name__ == "__main__":
    utils.main(go)
    sys.exit()
# }}}
