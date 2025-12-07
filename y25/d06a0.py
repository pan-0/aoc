# {{{
# Copyright 2025, pan (pan_@disroot.org)
# SPDX-License-Identifier: 0BSD

# vi: foldmethod=marker
from __future__ import annotations
from prelude import *
# }}}

Rows = list[list[int]]

def parse(itr: Iterator[str]) -> tuple[Rows, Iterator[str]]:
    lines = [*itr]
    filt = lambda line: filter(lambda ch: ch != '', line.split(' '))
    return ([*map(lambda line: [*map(int, filt(line))],
                  islice(lines, len(lines) - 1))],
            filt(lines[-1]))

def go(inp: Input) -> Iterator[int]:
    rows, ops = parse(inp)
    acc = 0
    for j, op in enumerate(ops):
        col = map(lambda row: row[j], rows)
        acc += {'+': sum, '*': prod}[op](col)
    yield acc

# {{{
if __name__ == "__main__":
    utils.main(go)
    sys.exit()
# }}}
