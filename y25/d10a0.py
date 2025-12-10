# {{{
# Copyright 2025, pan (pan_@disroot.org)
# SPDX-License-Identifier: 0BSD

# vi: foldmethod=marker
from __future__ import annotations
from prelude import *
# }}}
import z3

BIT_WIDTH = 16

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

def solve(machine: Machine) -> int:
    s = z3.Solver()

    coeffs = []
    rhs = z3.BitVecVal(0, BIT_WIDTH)
    for btn in machine.buttons:
        coeff = z3.BitVec(f"coeff_{len(coeffs)}", BIT_WIDTH)
        s.add(z3.And(coeff >= 0, coeff <= 1))
        rhs = rhs ^ (coeff * z3.BitVecVal(btn, BIT_WIDTH))
        coeffs.append(coeff)

    mask = z3.BitVecVal((1 << machine.bits) - 1, BIT_WIDTH)
    lights = z3.BitVecVal(machine.lights, BIT_WIDTH)
    s.add(lights == (rhs & mask))
    pushes = 0
    while s.check() == z3.sat:
        m = s.model()
        pushes = sum(map(lambda coeff: m[coeff].as_long(), coeffs))
        s.add(z3.Sum(coeffs) < pushes)
    return pushes

def go(inp: Input) -> Iterator[int]:
    data = parse(inp)
    acc = 0
    for machine in data:
        acc += solve(machine)
    yield acc

# {{{
if __name__ == "__main__":
    utils.main(go)
    sys.exit()
# }}}
