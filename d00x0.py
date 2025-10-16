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
    return map(str.strip, itr)

def go(inp: Input) -> Iterator[Any]:
    data = parse(inp)
    yield from data

# {{{
if __name__ == "__main__":
    utils.main(go)
    sys.exit()
# }}}
