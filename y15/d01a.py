# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

def f(s: str) -> int:
    return sum(map({'(': +1, ')': -1}.get, s))

def main():
    s = input()
    r = f(s)
    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit