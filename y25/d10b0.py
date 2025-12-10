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
    schematics: list[list[int]]
    jolts: list[int]

def parse(itr: Iterator[str]) -> Iterator[Machine]:
    for line in itr:
        parts = line.split(' ')
        schematics = []
        for schematic in parts[1:-1]:
            schematics.append([*map(int, schematic[1:-1].split(','))])

        jolts = [*map(int, parts[-1][1:-1].split(','))]
        yield Machine(schematics, jolts)

def solve(machine: Machine) -> int:
    s = z3.Solver()

    jolts_n = len(machine.jolts)
    coeffs = []
    sums = [[] for _ in range(jolts_n)]
    for schem in machine.schematics:
        coeff = z3.BitVec(f"coeff_{len(coeffs)}", BIT_WIDTH)
        s.add(coeff >= 0)
        for jolt_idx in schem:
            sums[jolt_idx].append(coeff)
        coeffs.append(coeff)

    for i in range(jolts_n):
        jolt = z3.BitVecVal(machine.jolts[i], BIT_WIDTH)
        s.add(z3.Sum(sums[i]) == jolt)
        for coeff in sums[i]:
            s.add(coeff <= jolt)

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
