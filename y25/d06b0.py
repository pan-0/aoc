# {{{
# Copyright 2025, pan (pan_@disroot.org)
# SPDX-License-Identifier: 0BSD

# vi: foldmethod=marker
from __future__ import annotations
from prelude import *
# }}}

Matrix = list[list[str]]

def transpose(mat: Matrix) -> Matrix:
    # [ 1 2 3 ]      [ 1 4 ]
    # [ 4 5 6 ]  ->  [ 2 5 ]
    #                [ 3 6 ]
    rows = len(mat)
    cols = len(mat[0])
    res = [[''] * rows for _ in range(cols)]
    for i in range(rows):
        for j in range(cols):
            res[j][i] = mat[i][j]
    return res

def go(inp: Input) -> Iterator[int]:
    data = [*map(lambda line: list(line.strip('\n')), inp)]
    mat = transpose(data)
    cols = len(mat[0])
    mat.append([' '] * cols)
    acc = 0
    i = 0
    while i < len(mat):
        op = {'+': sum, '*': prod}[mat[i][-1]]
        nums = []
        while (num := "".join(islice(mat[i], cols - 1)).strip()) != "":
            nums.append(int(num))
            i += 1
        acc += op(nums)
        i += 1
    yield acc

# {{{
if __name__ == "__main__":
    utils.main(go, strip=False)
    sys.exit()
# }}}
