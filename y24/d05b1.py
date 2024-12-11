# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

import fileinput
from collections import defaultdict
from dataclasses import dataclass, field
from functools import cmp_to_key, partial
from itertools import takewhile

@dataclass(frozen=True)
class Node:
    successors: set[int] = field(default_factory=set)

    def is_predecessor(self, num: int) -> bool:
        return num in self.successors

Vertices = dict[int, Node]

def parse(itr):
    rules = map(lambda line: map(int, line.strip().split('|')),
                takewhile(lambda line: line != "\n", itr))
    V = defaultdict(Node)
    for lhs, rhs in rules:
        V[lhs].successors.add(rhs)

    updates = map(lambda line: map(int, line.strip().split(',')), itr)
    return (V, updates)

Update = list[int]

def update_bad(V: Vertices, update: Update) -> bool:
    length = len(update)
    for i in range(length - 1):
        v = V.get(update[i])
        if v is None or any(map(lambda j: not v.is_predecessor(update[j]),
                                range(i + 1, length))):
            return True
    return False

def update_fixed(V: Vertices, update: Update) -> Update:
    cmp = lambda vi, w: \
        -1 if (v := V.get(vi)) is not None and v.is_predecessor(w) else 1
    return sorted(update, key=cmp_to_key(cmp))

def solve(V: Vertices, updates) -> int:
    return sum(map(lambda upd: update_fixed(V, upd)[len(upd) // 2],
                   filter(partial(update_bad, V), map(list, updates))))

def main():
    V, updates = parse(fileinput.input())
    r = solve(V, updates)
    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit