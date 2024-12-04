# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

import hashlib
from functools import partial

def first(itr, key=lambda x: True):
    return next(filter(key, itr))

def f(key: str, n: int):
    inp = (key + str(n)).encode("ascii")
    return (
        int.from_bytes(hashlib.md5(inp).digest()[:3]) & 0xFFFFF0 == 0,
        n
    )

def main():
    N = 1 << 31
    key = input()
    r = first(map(partial(f, key), range(N)), key=lambda p: p[0])
    print(r[1])

if __name__ == "__main__":
    main()
    raise SystemExit