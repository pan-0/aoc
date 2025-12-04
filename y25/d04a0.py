# {{{
# Copyright (C) 2025 by pan <pan_@disroot.org>
# SPDX-License-Identifier: 0BSD

# vi: foldmethod=marker
from __future__ import annotations
from prelude import *

Grid = utils.Grid[str]
# }}}

def go(inp: Input) -> Iterator[int]:
    grid = Grid([*inp])
    acc = 0
    for i in range(grid.rows):
        for j in range(grid.cols):
            if grid[i, j] == '@':
                adj_rolls = ilen(filter(lambda adj: grid[adj] == '@',
                                        grid.adjacent((i, j))))
                if adj_rolls < 4:
                    acc += 1
    yield acc

# {{{
if __name__ == "__main__":
    utils.main(go)
    sys.exit()
# }}}
