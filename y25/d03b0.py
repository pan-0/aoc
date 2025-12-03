# {{{
# Copyright (C) 2025 by pan <pan_@disroot.org>
# SPDX-License-Identifier: 0BSD

# vi: foldmethod=marker
from __future__ import annotations
from prelude import *
# }}}

def parse(itr: Iterator[str]) -> Iterator[list[str]]:
    return map(list, itr)

def xmax(bank: list[str], start: int, end: int) -> int:
    x = start
    for i in range(x + 1, end):
        if bank[i] > bank[x]:
            x = i
    return x

def go(inp: Input) -> Iterator[int]:
    acc = 0
    for bank in parse(inp):
        bats = []
        start = 0
        for i in range(12 - 1, -1, -1):
            x = xmax(bank, start, len(bank) - i)
            start = x + 1
            bats.append(bank[x])
        acc += int("".join(bats))
    yield acc

# {{{
if __name__ == "__main__":
    utils.main(go)
    sys.exit()
# }}}
