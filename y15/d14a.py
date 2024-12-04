# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

import fileinput
from dataclasses import dataclass

@dataclass(frozen=True)
class Triple:
    speed: int
    dur: int
    rest: int

def parse(s: str) -> Triple:
    parts = s.split(' ')
    return Triple(*map(lambda i: int(parts[i]), (3, 6, 13)))

@dataclass
class State:
    rem: int            # Remaining time
    dist: int = 0       # Distance covered
    rest: bool = False  # In resting state?

def solve(triples: list[Triple], t_end: int) -> int:
    states = [*map(lambda t: State(t.dur), triples)]
    for t in range(t_end):
        for state, triple in zip(states, triples):
            state.rem -= 1
            if not state.rest:
                state.dist += triple.speed

            if state.rem == 0:
                state.rem = triple.dur if state.rest else triple.rest
                state.rest ^= True

    return max(states, key=lambda s: s.dist).dist

def main():
    triples = sorted(map(parse, fileinput.input()), key=lambda t: t.dur)
    r = solve(triples, 2503)
    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit