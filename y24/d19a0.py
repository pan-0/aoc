# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

import fileinput
import re
from typing import Iterator

def parse(itr) -> tuple[list[str], Iterator[str]]:
    patterns = next(itr).strip().split(", ")
    _ = next(itr)
    return (patterns, map(str.strip, itr))

def main():
    patterns, towels = parse(fileinput.input())
    regex = re.compile(f"({'|'.join(patterns)})+")
    r = sum(map(lambda towel: regex.fullmatch(towel) is not None, towels))
    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit
