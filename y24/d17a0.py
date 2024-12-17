# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

import fileinput
from utils import integers, take, unreachable

Registers = list[int]
Instructions = list[int]

def parse(itr) -> tuple[Registers, Instructions]:
    nums = integers(itr)
    # A: 0, B: 1, C: 2
    regs = [*take(nums, 3)]
    insns = [*nums]
    return (regs, insns)

def operand(regs: Registers, opr: int) -> int:
    match opr:
        case lit if 0 <= lit <= 3: return lit
        case reg if 4 <= reg <= 6: return regs[reg - 4]
        case _:
            unreachable("invalid operand: ", opr)

def run(regs: Registers, insns: Instructions) -> list[int]:
    out = []
    ip = 0
    while ip < len(insns):
        opr = insns[ip + 1]
        match insns[ip]:
            case 0:  # adv
                regs[0] >>= operand(regs, opr)
            case 1:  # bxl
                regs[1] ^= opr
            case 2:  # bst
                regs[1] = operand(regs, opr) & 7
            case 3:  # jnz
                if regs[0] != 0:
                    ip = opr
                    continue
            case 4:  # bxc
                regs[1] ^= regs[2]
            case 5:  # out
                out.append(operand(regs, opr) & 7)
            case 6:  # bdv
                regs[1] = regs[0] >> operand(regs, opr)
            case 7:  # cdv
                regs[2] = regs[0] >> operand(regs, opr)
            case _:
                unreachable("invalid instruction: ", insns[i])
        ip += 2
    return out

def main():
    regs, insns = parse(fileinput.input())
    out = run(regs, insns)
    r = ",".join(map(str, out))
    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit
