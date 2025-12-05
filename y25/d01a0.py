# {{{
# Copyright (C) 2025 by pan <pan_@disroot.org>
# SPDX-License-Identifier: 0BSD

# vi: foldmethod=marker
from __future__ import annotations
from prelude import *
# }}}

def parse(itr: Iterator[str]) -> Iterator[int]:
    return map(lambda line: {'L': -1, 'R': 1}[line[0]] * int(line[1:]), itr)

def go(inp: Input) -> Iterator[int]:
    data = parse(inp)
    dial = 50
    count = 0
    for rot in data:
        dial = (dial + rot) % 100
        count += dial == 0
    yield count

# {{{
if __name__ == "__main__":
    utils.main(go)
    sys.exit()
# }}}
