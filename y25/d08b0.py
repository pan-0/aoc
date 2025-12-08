# {{{
# Copyright 2025, pan (pan_@disroot.org)
# SPDX-License-Identifier: 0BSD

# vi: foldmethod=marker
from __future__ import annotations
from prelude import *
# }}}
class Box(NamedTuple):
    x: int
    y: int
    z: int

def parse(itr: Iterator[str]) -> Iterator[Box]:
    return map(lambda line: Box(*map(int, line.split(',')),), itr)

def dist_sqr(a: Box, b: Box) -> int:
    return (a.x - b.x)**2 + (a.y - b.y)**2 + (a.z - b.z)**2

def parent(circuits: list[int], x: int) -> int:
    while circuits[x] != x:
        y = circuits[x]
        circuits[x] = circuits[y]
        x = y
    return x

def go(inp: Input) -> Iterator[int]:
    boxes = dict(starmap(lambda i, box: (box, i), enumerate(parse(inp))))
    closest = sorted(combinations(boxes.keys(), 2),
                     key=lambda pair: dist_sqr(*pair))
    circuits = [*range(len(boxes))]
    for a, b in closest:
        circuits[parent(circuits, boxes[b])] = boxes[a]
        for i in range(len(circuits)):
            circuits[i] = parent(circuits, i)

        if len(set(circuits)) == 1:
            yield a.x * b.x
            return

# {{{
if __name__ == "__main__":
    utils.main(go)
    sys.exit()
# }}}
