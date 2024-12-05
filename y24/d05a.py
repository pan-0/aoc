# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

import fileinput
from dataclasses import dataclass, field
from functools import partial
from itertools import takewhile

@dataclass(frozen=True)
class Node:
    num: int
    successors: set[int] = field(default_factory=set)

    def is_predecessor(self, num: int) -> bool:
        return num in self.successors

Vertices = dict[int, Node]

def parse(itr):
    rules = map(lambda line: map(int, line.strip().split('|')),
                takewhile(lambda line: line != "\n", itr))
    V = {}
    for lhs, rhs in rules:
        v = V.get(lhs)
        if v is None:
            v = V[lhs] = Node(lhs)
        v.successors.add(rhs)

    updates = map(lambda line: map(int, line.strip().split(',')), itr)
    return (V, updates)

Update = list[int]

def update_ok(V: Vertices, update: Update) -> bool:
    length = len(update)
    for i in range(length - 1):
        v = V.get(update[i])
        if v is None or any(map(lambda j: not v.is_predecessor(update[j]),
                                range(i + 1, length))):
            return False
    return True

def solve(V: Vertices, updates) -> int:
    return sum(map(lambda upd: upd[len(upd) // 2],
                   filter(partial(update_ok, V), map(list, updates))))

def main():
    V, updates = parse(fileinput.input())
    r = solve(V, updates)
    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit