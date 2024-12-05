# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

import json
from collections import deque

def f(doc) -> int:
    acc = 0
    queue = deque((doc,))
    while queue:
        obj = queue.popleft()
        if isinstance(obj, int):
            acc += obj
        elif isinstance(obj, list):
            queue.extend(obj)
        elif isinstance(obj, dict):
            queue.extend(obj.values())
        elif isinstance(obj, str) or isinstance(obj, float):
            pass
        else:
            raise ValueError
    return acc

def main():
    s = input()
    doc = json.loads(s)
    r = f(doc)
    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit