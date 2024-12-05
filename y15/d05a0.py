# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

import fileinput
import string

VOWELS = frozenset("aeiou")
DOUBLES = (*map(lambda c: 2 * c, string.ascii_lowercase),)

def nice(s: str) -> bool:
    return \
        len(VOWELS.intersection(frozenset(s))) >= 3 and \
        any(map(lambda cc: cc in s, DOUBLES)) and \
        all(map(lambda cc: cc not in s, ("ab", "cd", "pq", "xy")))

def main():
    r = sum(map(nice, fileinput.input()))
    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit