# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

import fileinput
from itertools import takewhile

def double(s: str) -> tuple[str, str]:
    parts = s.split(" => ")
    return (parts[0], parts[1][:-1])

Replacements = list[tuple[str, str]]

def parse(itr) -> tuple[Replacements, str]:
    replacements = [*map(double, takewhile(lambda line: line != "\n", itr))]
    return (replacements, next(itr)[:-1])

def solve(replacements: Replacements, molecule: str) -> int:
    molecules = set()
    for target, rep in replacements:
        pos = 0
        while (pos := molecule.find(target, pos)) >= 0:
            new = "".join((molecule[:pos], rep, molecule[pos + len(target):]))
            molecules.add(new)
            pos += len(target)
    return len(molecules)

def main():
    replacements, molecule = parse(fileinput.input())
    r = solve(replacements, molecule)
    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit