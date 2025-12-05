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

def union(A: Range, B: Range) -> Optional[Range]:
    for X, Y in (A, B), (B, A):
        if Y.a <= X.a <= Y.b:
            if X.b <= Y.b:
                return Y
            else:
                return Range(Y.a, X.b)

        if Y.a <= X.b <= Y.b:
            assert X.a < Y.a
            return Range(X.a, Y.b)
    return None

def add_range(sets: list[Range], R: Range):
    for i, curr in enumerate(sets):
        u = union(curr, R)
        if u is not None:
            sets.pop(i)
            add_range(sets, u)
            break
    else:
        sets.append(R)

def go(inp: Input) -> Iterator[int]:
    ranges = parse(inp)
    sets = []
    for rng in ranges:
        add_range(sets, rng)
    res = sum(map(lambda rng: rng.b - rng.a + 1, sets))
    yield res

# {{{
if __name__ == "__main__":
    utils.main(go)
    sys.exit()
# }}}
