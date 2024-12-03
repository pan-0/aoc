# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

import fileinput

def parse(itr):
    return map(lambda line: map(int, line.strip().split("   ")), itr)

def main():
    L, R = map(sorted, zip(*parse(fileinput.input())))
    r = sum(map(lambda x, y: abs(x - y), L, R))
    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit
