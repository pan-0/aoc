# {{{
# Copyright 2025, pan (pan_@disroot.org)
# SPDX-License-Identifier: 0BSD

# vi: foldmethod=marker
from __future__ import annotations
from prelude import *

Grid = utils.Grid[str]
# }}}

def go(inp: Input) -> Iterator[str]:
    grid = Grid([*inp])
    beams = Counter((grid.find('S'),))
    timelines = 1
    while beams:
        new_beams = Counter()
        for beam, count in beams.items():
            fw = beam + Adjacents.DOWN.vec
            if grid.is_inbounds(fw):
                if grid[fw] == '^':
                    left = fw + Adjacents.LEFT.vec
                    right = fw + Adjacents.RIGHT.vec
                    new_beams[left] += count
                    new_beams[right] += count
                    timelines += count
                else:
                    new_beams[fw] += count
        beams = new_beams
    yield timelines

# {{{
if __name__ == "__main__":
    utils.main(go)
    sys.exit()
# }}}
