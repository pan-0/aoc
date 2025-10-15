# {{{
# vi: foldmethod=marker
# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

from __future__ import annotations
from prelude import *

Vec2: TypeAlias = utils.Vec2[int]
dprint = utils.DebugPrint()
# }}}
@dataclass(frozen=True)
class Room:
    name: str
    sector: int
    chksum: str

def parse(itr: Iterator[str]) -> Iterator[Room]:
    for line in map(str.strip, itr):
        if line != "":
            parts = line.split('-')
            last = parts[-1]
            lb = last.find('[')
            sector = int(last[:lb])
            chksum = last[lb:][1:-1]
            yield Room("".join(parts[:-1]), sector, chksum)

def go(inp: Input) -> Iterator[int]:
    acc = 0
    inp = parse(inp)
    for room in inp:
        hist = Counter(room.name)
        first = hist.most_common(1)[0][1]
        comp = "".join(starmap(lambda k, _v: k,
                               sorted(hist.items(),
                                      key=lambda kv: (first - kv[1], kv[0]))))
        if comp.startswith(room.chksum):
            acc += room.sector
    yield acc

# {{{
if __name__ == "__main__":
    utils.main(go)
    sys.exit()
# }}}
