# {{{
# Copyright 2025, pan (pan_@disroot.org)
# SPDX-License-Identifier: 0BSD

# vi: foldmethod=marker
from __future__ import annotations
from prelude import *
# }}}

@dataclass(frozen=True)
class Machine:
    bits: int
    lights: int
    buttons: list[int]

def parse(itr: Iterator[str]) -> Iterator[Machine]:
    for line in itr:
        parts = line.split(' ')
        lights = 0
        bits = 0
        for i, light in enumerate(parts[0][1:-1]):
            bits += 1
            lights |=  {'.': 0, '#': 1}[light] << i

        buttons = []
        for button in parts[1:-1]:
            btn_val = 0
            for idx in map(int, button[1:-1].split(',')):
                btn_val |= 1 << idx
            buttons.append(btn_val)

        yield Machine(bits, lights, buttons)

def do_add(s: set[int], e: int) -> bool:
    l = len(s)
    s.add(e)
    return l != len(s)

def solve(machine: Machine) -> int:
    mask = (1 << machine.bits) - 1
    visited = set()
    queue = deque([(0, 0)])
    while queue:
        state, depth = queue.popleft()
        if do_add(visited, state):
            if state & mask == machine.lights:
                return depth

            queue.extend(map(lambda button: (state ^ button, depth + 1),
                             machine.buttons))
    return pushes

def go(inp: Input) -> Iterator[int]:
    data = parse(inp)
    acc = sum(map(solve, data))
    yield acc

# {{{
if __name__ == "__main__":
    utils.main(go)
    sys.exit()
# }}}
