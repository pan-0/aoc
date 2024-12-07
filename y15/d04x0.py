# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

import hashlib
import sys
from functools import partial
from itertools import islice

def first(itr, key=lambda x: True):
    return next(filter(key, itr))

def f(secret: str, mask: int, n: int) -> bool:
    inp = f"{secret}{n}".encode("ascii")
    md5 = hashlib.md5(inp).digest()
    return int.from_bytes(islice(md5, 3), byteorder="big") & mask == 0

def main():
    N = 1 << 31
    secret = sys.argv[1]
    ra = first(range( 0, N), key=partial(f, secret, 0xFFFFF0))
    rb = first(range(ra, N), key=partial(f, secret, 0xFFFFFF))
    print(ra, rb)

if __name__ == "__main__":
    main()
    sys.exit()