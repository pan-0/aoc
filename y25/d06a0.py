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
    filt = lambda line: filter(lambda ch: ch != '' and ch != ' ',
                               line.split(' '))
    return ([*map(lambda line: [*map(pipe(str.strip, int), filt(line))],
                  islice(lines, len(lines) - 1))],
            filt(lines[-1]))

def column(rows: Rows, j: int) -> Iterator[int]:
    for row in rows:
        yield row[j]

def go(inp: Input) -> Iterator[int]:
    rows, ops = parse(inp)
    acc = 0
    for j, op in enumerate(ops):
        acc += {'+': sum, '*': prod}[op](column(rows, j))
    yield acc

# {{{
if __name__ == "__main__":
    utils.main(go)
    sys.exit()
# }}}
