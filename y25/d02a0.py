# {{{
# Copyright (C) 2025 by pan <pan_@disroot.org>
# SPDX-License-Identifier: 0BSD

# vi: foldmethod=marker
from __future__ import annotations
from prelude import *

Vec2: TypeAlias = utils.Vec2[int]
dprint = utils.DebugPrint()
# }}}

def parse(line) -> Iterator[tuple[int, int]]:
    return map(lambda rng: (*map(int, rng.split('-')),), line.split(','))

def go(inp: Input) -> Iterator[int]:
    data = parse(next(inp))
    invalid = 0
    for a, b in data:
        for i in range(a, b + 1):
            s = str(i)
            if len(s) & 1 == 0 and s[:len(s) // 2] == s[len(s) // 2:]:
                invalid += i
    yield invalid

# {{{
if __name__ == "__main__":
    utils.main(go)
    sys.exit()
# }}}
