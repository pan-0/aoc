# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

def f(s: str) -> int:
    a = 0
    for i, c in enumerate(s, start=1):
        a += {'(': +1, ')': -1}[c]
        if a < 0:
            return i

    return 0

def main():
    s = input()
    r = f(s)
    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit