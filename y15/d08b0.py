# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

import fileinput

def main():
    T = str.maketrans({'\\': r"\\", '"':  r"\""})
    enc = orig = 0
    for s in map(lambda line: f'"{line.strip()}"', fileinput.input()):
        e = s.translate(T)
        enc += len(e)
        orig += len(s)

    r = enc - orig
    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit