# {{{
# Copyright (C) 2025 by pan <pan_@disroot.org>
# SPDX-License-Identifier: 0BSD

# vi: foldmethod=marker
from __future__ import annotations
from prelude import *

Vec2: TypeAlias = utils.Vec2[int]
dprint = utils.DebugPrint()
# }}}

def parse(itr: Iterator[str]) -> Iterator[Any]:
    return map(list, itr)

def go(inp: Input) -> Iterator[Any]:
    acc = 0
    for bank in parse(inp):
        first = max(bank[:-1])
        index = bank.index(first)
        second = max(bank[index + 1:])
        acc += int(f"{first}{second}")
    yield acc

# {{{
if __name__ == "__main__":
    utils.main(go)
    sys.exit()
# }}}
