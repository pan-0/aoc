# {{{
# Copyright (C) 2025 by pan <pan_@disroot.org>
# SPDX-License-Identifier: 0BSD

# vi: foldmethod=marker
from __future__ import annotations
from prelude import *

Grid = utils.MutGrid[str]
# }}}

def rolls(grid: Grid) -> list[tuple[int, int]]:
    rem = []
    for i in range(grid.rows):
        for j in range(grid.cols):
            if grid[i, j] == '@':
                adj_rolls = ilen(filter(lambda adj: grid[adj] == '@',
                                        grid.adjacent((i, j))))
                if adj_rolls < 4:
                    rem.append((i, j))
    return rem

def go(inp: Input) -> Iterator[int]:
    grid = Grid([*map(list, inp)])
    acc = 0
    rem = rolls(grid)
    while rem:
        for (i, j) in rem:
            grid[i, j] = '.'
        acc += len(rem)
        rem = rolls(grid)
    yield acc

# {{{
if __name__ == "__main__":
    utils.main(go)
    sys.exit()
# }}}
