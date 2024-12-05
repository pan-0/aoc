# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

import ast
import fileinput

def main():
    chars = mem = 0
    for s in map(str.strip, fileinput.input()):
        p = ast.literal_eval(s)
        chars += len(s)
        mem += len(p)

    r = chars - mem
    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit