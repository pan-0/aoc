# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

import sys
from itertools import islice

def lns(n: bytearray) -> bytearray:
    r = bytearray()
    count = 0
    dig = n[0]
    for ndig in n:
        if ndig != dig:
            r.extend((count - 1, dig))
            dig = ndig
            count = 0
        count += 1
    r.extend((count - 1, dig))
    return r

def main():
    start, iters = sys.argv[1:3]
    n = bytearray(map(lambda dig: ord(dig) - ord('1'), start))
    for _ in range(int(iters)):
        n = lns(n)

    r = len(n)
    print(r)

if __name__ == "__main__":
    main()
    sys.exit()