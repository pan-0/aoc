# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

import fileinput
from itertools import islice, starmap
from dataclasses import dataclass
from typing import Optional

try:
    from itertools import batched
except ImportError:
    def batched(itr, n, *, strict=False):
        # batched("ABCDEFG", 3) -> ABC DEF G
        if n < 1:
            raise ValueError("n must be at least one")
        it = iter(itr)
        while batch := (*islice(it, n),):
            if strict and len(batch) != n:
                raise ValueError("batched(): incomplete batch")
            yield batch

@dataclass(frozen=True)
class Machine:
    ax: int
    ay: int
    bx: int
    by: int
    px: int
    py: int

def parse(itr) -> Machine:
    lines = map(lambda tup: tup[0].strip(), zip(itr, range(3)))
    a = next(lines).split(", ")
    ax = int(a[0][a[0].find('+') + 1:])
    ay = int(a[1][a[1].find('+') + 1:])
    b = next(lines).split(", ")
    bx = int(b[0][b[0].find('+') + 1:])
    by = int(b[1][b[1].find('+') + 1:])
    p = next(lines).split(", ")
    px = int(p[0][p[0].find('=') + 1:]) + 10000000000000
    py = int(p[1][p[1].find('=') + 1:]) + 10000000000000
    return Machine(ax, ay, bx, by, px, py)

def win_comb(m: Machine) -> Optional[tuple[int, int]]:
    denom = m.bx * m.ay - m.ax * m.by
    if denom != 0:
        xa = (m.bx * m.py - m.px * m.by) / denom
        xb = (m.px * m.ay - m.ax * m.py) / denom
        if all(map(float.is_integer, (xa, xb))):
            pushes = (*map(int, (xa, xb)),)
            if all(map(lambda push: push >= 0, pushes)):
                return pushes
    return None

def main():
    machines = map(parse, batched(fileinput.input(), 4))
    r = sum(starmap(lambda xa, xb: 3 * xa + xb,
                    filter(lambda comb: comb is not None,
                           map(win_comb, machines))))
    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit
