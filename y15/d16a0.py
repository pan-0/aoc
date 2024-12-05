# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

from __future__ import annotations

import fileinput
from dataclasses import dataclass
from itertools import chain
from operator import eq
from typing import NamedTuple, Optional

class Compounds(NamedTuple):
    children:    Optional[int] = None
    cats:        Optional[int] = None
    samoyeds:    Optional[int] = None
    pomeranians: Optional[int] = None
    akitas:      Optional[int] = None
    vizslas:     Optional[int] = None
    goldfish:    Optional[int] = None
    trees:       Optional[int] = None
    cars:        Optional[int] = None
    perfumes:    Optional[int] = None

    def __eq__(self, other: Compounds) -> bool:
        return all(map(lambda pair: eq(*pair),
                       filter(lambda xy: all(map(lambda v: v is not None, xy)),
                              zip(self, other))))

@dataclass(frozen=True)
class Sue:
    num: int
    compounds: Compounds

def parse(s: str) -> Sue:
    colon = s.find(':')
    num = int(s[4:colon])
    compounds = map(lambda comp: comp.split(": "), s[colon + 2:-1].split(", "))
    return Sue(num, Compounds(**dict(map(lambda compval: \
                                            (compval[0], int(compval[1])),
                                         compounds))))

def main():
    sues = map(parse, fileinput.input())
    aunt = Compounds(children=3,
                     cats=7,
                     samoyeds=2,
                     pomeranians=3,
                     akitas=0,
                     vizslas=0,
                     goldfish=5,
                     trees=3,
                     cars=2,
                     perfumes=1)
    r = next(chain(filter(lambda sue: sue.compounds == aunt, sues), (None,)))
    if r is not None:
        print(r.num)

if __name__ == "__main__":
    main()
    raise SystemExit