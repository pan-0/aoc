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
    def f(begin: str, df: int) -> int:
        out_df = df | (begin == "dac") << 1 | (begin == "fft")
        return (begin == "out" and df == 0x3) \
               + sum(map(lambda out: f(out, out_df), data[begin]))
    yield f("svr", 0)

# {{{
if __name__ == "__main__":
    utils.main(go)
    sys.exit()
# }}}
