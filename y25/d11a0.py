# {{{
# Copyright 2025, pan (pan_@disroot.org)
# SPDX-License-Identifier: 0BSD

# vi: foldmethod=marker
from __future__ import annotations
from prelude import *
# }}}

def parse(itr: Iterator[str]) -> dict[str, list[str]]:
    devs = {"out": []}
    for line in itr:
        parts = line.split(' ')
        rule = parts[0][:-1]
        devs[rule] = parts[1:]
    return devs

def go(inp: Input) -> Iterator[int]:
    data = parse(inp)
    @cache
    def f(begin: str) -> int:
        return (begin == "out") + sum(map(f, data[begin]))
    yield f("you")

# {{{
if __name__ == "__main__":
    utils.main(go)
    sys.exit()
# }}}
