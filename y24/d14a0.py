# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

import fileinput
from utils import MutGrid, Vec2, batched, integers

Positions = list[Vec2[int]]
Velocities = list[Vec2[int]]

def parse(itr) -> tuple[Positions, Velocities]:
    nums = batched(integers(itr), 4)
    P = []
    V = []
    for px, py, vx, vy in nums:
        P.append(Vec2(px, py))
        V.append(Vec2(vx, vy))
    return (P, V)

def main():
    P, V = parse(fileinput.input())
    G = MutGrid.empty(103, 101, 0)
    for pos in P:
        G[pos] += 1

    for _ in range(100):
        for (i, pos), vel in zip(enumerate(P), V):
            G[pos] -= 1
            pos = P[i] = (pos + vel) % Vec2(G.cols, G.rows)
            G[pos] += 1

    r = 1
    quad_rows = G.rows // 2
    quad_cols = G.cols // 2
    for quad_x, quad_y in (0, 0), (0, quad_cols + 1), \
                          (quad_rows + 1, 0), (quad_rows + 1, quad_cols + 1):
        acc = 0
        for i in range(quad_rows):
            for j in range(quad_cols):
                acc += G[quad_x + i, quad_y + j]
        r *= acc

    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit
