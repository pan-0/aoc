# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

import sys
from string import ascii_lowercase

BLOCKED: str = "iol"

def base0(ch: str) -> int:
    return ord(ch) - ord('a')

def sequence() -> list[int]:
    seq = [*map(lambda c: base0(c) + 1, ascii_lowercase)]
    # Patch out blocked characters.
    for c in BLOCKED:
        seq[base0(c) - 1] = seq[base0(c)]

    seq[-1] = 0  # For wrap-around.
    return seq

class Numbers:
    SEQUENCE = sequence()

    def __init__(self, passw: str):
        self.nums = self.numbers(passw)

    @staticmethod
    def numbers(passw: str) -> list[int]:
        nums = [*map(base0, passw)]
        try:
            blocked = min(filter(lambda i: i >= 0, map(passw.find, BLOCKED)))
        except ValueError:
            pass
        else:
            nums[blocked] = Numbers.SEQUENCE[nums[blocked]]
            for i in range(blocked + 1, len(nums)):
                nums[i] = 0
        return nums

    def req_1(self) -> bool:
        nums = self.nums
        i = 0
        end = len(nums) - 3 + 1
        while i < end:
            for j in range(i, i + 2):
                k = j + 1
                if nums[k] != nums[j] + 1:
                    i = k
                    break
            else:
                return True
        return False

    def req_3(self) -> bool:
        nums = self.nums
        first: int
        offset: int
        length = len(nums)
        for i in range(length - (1 + 2)):
            first = nums[i]
            if first == nums[i + 1]:
                offset = i + 2
                break
        else:
            return False

        for i in range(offset, length - 1):
            sec = nums[i]
            if first != sec and sec == nums[i + 1]:
                return True

        return False

    def advance(self):
        nums = self.nums
        for i in range(len(nums) - 1, -1, -1):
            val = nums[i] = self.SEQUENCE[nums[i]]
            if val != 0:
                break

    def __str__(self) -> str:
        return "".join(map(lambda n: chr(n + ord('a')), self.nums))

def main():
    passw = sys.argv[1]
    nums = Numbers(passw)
    while True:
        nums.advance()
        if nums.req_1() and nums.req_3():
            break

    print(nums)

if __name__ == "__main__":
    main()
    sys.exit()