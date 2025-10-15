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
            yield Room("-".join(parts[:-1]), sector, chksum)

def rotate_letter(letter: str, n: int) -> str:
    assert letter.islower()
    return chr(((ord(letter) - ord('a') + n) % 26) + ord('a'))

def rotate(s: str, n: int) -> str:
    return "".join(map(lambda c: ' ' if c in " -" else rotate_letter(c, n), s))

def go(inp: Input) -> Iterator[tuple[str, int]]:
    acc = 0
    data = parse(inp)
    for room in data:
        hist = Counter(filter(lambda letter: letter != '-', room.name))
        first = hist.most_common(1)[0][1]
        comp = "".join(starmap(lambda k, _v: k,
                               sorted(hist.items(),
                                      key=lambda kv: (first - kv[1], kv[0]))))
        if comp.startswith(room.chksum):
            decrypted = rotate(room.name, room.sector)
            if "object" in decrypted:
                yield (decrypted, room.sector)

# {{{
if __name__ == "__main__":
    utils.main(go, unpack=True)
    sys.exit()
# }}}
