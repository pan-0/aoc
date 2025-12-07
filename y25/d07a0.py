# {{{
# Copyright 2025, pan (pan_@disroot.org)
# SPDX-License-Identifier: 0BSD

# vi: foldmethod=marker
from __future__ import annotations
from prelude import *

Grid = utils.Grid[str]
# }}}

def go(inp: Input) -> Iterator[int]:
    grid = Grid([*inp])
    beams = {grid.find('S')}
    splits = 0
    while beams:
        new_beams = set()
        for beam in beams:
            fw = beam + Adjacents.DOWN.vec
            if grid.is_inbounds(fw):
                if grid[fw] == '^':
                    left = fw + Adjacents.LEFT.vec
                    right = fw + Adjacents.RIGHT.vec
                    new_beams.update((left, right))
                    splits += 1
                else:
                    new_beams.add(fw)
        beams = new_beams
    yield splits

# {{{
if __name__ == "__main__":
    utils.main(go)
    sys.exit()
# }}}
