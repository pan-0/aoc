import fileinput
import sys
import z3
from itertools import islice
from utils import integers, unreachable

Instructions = list[int]

BIT_WIDTH = 64

def parse(itr) -> Instructions:
    nums = integers(itr)
    return [*islice(nums, 3, None)]

def operand(regs, opr: int):
    match opr:
        case lit if 0 <= lit <= 3: return z3.BitVecVal(lit, BIT_WIDTH) & 3
        case reg if 4 <= reg <= 6: return regs[reg - 4]
        case _:
            unreachable("invalid operand: ", opr)

def run(regs, insns: Instructions, out: int):
    for i in range(0, len(insns), 2):
        opr = insns[i + 1]
        match insns[i]:
            case 0:  # adv
                regs[0] = regs[0] >> operand(regs, opr)
            case 1:  # bxl
                regs[1] = regs[1] ^ (z3.BitVecVal(opr, BIT_WIDTH) & 7)
            case 2:  # bst
                regs[1] = operand(regs, opr) & 7
            case 3:  # jnz
                pass
            case 4:  # bxc
                regs[1] = regs[1] ^ regs[2]
            case 5:  # out
                return operand(regs, opr) & 7 == insns[out]
            case 6:  # bdv
                regs[1] = regs[0] >> operand(regs, opr)
            case 7:  # cdv
                regs[2] = regs[0] >> operand(regs, opr)
            case _:
                unreachable("invalid instruction: ", insns[i])
    unreachable()

def main():
    insns = parse(fileinput.input())
    A = z3.BitVec('A', BIT_WIDTH)
    regs = [A, z3.BitVecVal(0, BIT_WIDTH), z3.BitVecVal(0, BIT_WIDTH)]

    s = z3.Solver()
    s.add(z3.UGT(A, 0))
    for i in range(len(insns)):
        s.add(run(regs, insns, i))
    s.add(regs[0] == 0)

    r = 0
    while s.check() == z3.sat:
        m = s.model()
        r = m[A]
        s.add(z3.ULT(A, m[A]))

    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit