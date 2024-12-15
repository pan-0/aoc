# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

from __future__ import annotations

import copy
import io
import math
import operator
import re
from collections import deque
from collections.abc import Iterator, MutableSequence, Sequence
from dataclasses import dataclass
from functools import partialmethod
from itertools import chain, islice
from typing import Generic, NamedTuple, Optional, Self, TypeVar

T = TypeVar("T")
U = TypeVar("U")

try:
    from itertools import batched  # type: ignore[attr-defined]
except ImportError:
    def batched(itr: Iterator[T], n: int, *, strict=False) \
            -> Iterator[tuple[T, ...]]:
        # batched("ABCDEFG", 3) -> ABC DEF G
        if n < 1:
            raise ValueError("n must be at least one")
        it = iter(itr)
        while batch := (*islice(it, n),):
            if strict and len(batch) != n:
                raise ValueError("batched(): incomplete batch")
            yield batch

def integers(itr: Iterator[str], signed=True) -> Iterator[int]:
    uint_pat = r"(?:0|[1-9]\d*)"
    pat = fr"(-?{uint_pat})" if signed else fr"({uint_pat})"
    nums = chain.from_iterable(map(lambda s: re.finditer(pat, s), itr))
    return map(lambda match: int(match[0]), nums)

def ceildiv(x: int, y: int) -> int:
    assert x > 0
    return 1 + (x - 1) // y

def first(itr: Iterator[T], key=lambda x: True) -> Optional[T]:
    return next(chain(filter(key, itr), (None,)))

def last(itr: Iterator[T], key=lambda x: True) -> Optional[T]:
    r = None
    for x in filter(key, itr):
        r = x
    return r

def take(itr: Iterator[T], n: int, *, strict=False) -> Iterator[T]:
    # take("ABCDEFG",  3) -> ABC
    # take("ABCDEFG",  0) ->
    # take("ABCDEFG", -1) -> ABCDEFG
    if n < -1:
        raise ValueError("n must be int [-1, +inf)")
    it = iter(itr)
    i = 0
    for i, x in enumerate(it):
        if i == n:
            break
        yield x
    if strict and n != -1 and i != n:
        raise ValueError("take(): incomplete iterator")

def ilen(itr: Iterator[T]) -> int:
    i = 0
    for i, _ in enumerate(itr, start=1):
        pass
    return i

def identity(x: T) -> T:
    return x

def joinlines(itr: Iterator[str], strip=True) -> str:
    return "".join(map(str.strip if strip else identity, itr))

class DebugPrint:
    def __init__(self, enabled=True):
        self.enabled = enabled

    def on(self):
        self.enabled = True

    def off(self):
        self.enabled = False

    def toggle(self):
        self.enabled ^= True

    def __call__(self, *args, **kwargs):
        if self.enabled:
            print(*args, **kwargs)

class Pair(NamedTuple, Generic[T, U]):
    f: T
    s: U

    def __hash__(self) -> int:
        return hash(self.f) ^ hash(self.s)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Pair):
            raise ValueError
        return {self.f, self.s} == {other.f, other.s}

N = TypeVar("N", int, float)

@dataclass(frozen=True)
class Vec(Generic[N]):
    scalars: tuple[N, ...]

    def __init__(self, *args: N):
        object.__setattr__(self, "scalars", args)

    def __iter__(self):
        return iter(self.scalars)

    def __add__(self, other: Self) -> Self:
        return type(self)(*map(operator.add, self, other))

    def __sub__(self, other: Self) -> Self:
        return type(self)(*map(operator.sub, self, other))

    def __mul__(self, other: Self) -> Self:
        return type(self)(*map(operator.mul, self, other))

    def __mod__(self, other: Self) -> Self:
        return type(self)(*map(operator.mod, self, other))

    def __floordiv__(self, other: Self) -> Self:
        return type(self)(*map(operator.floordiv, self, other))

    def __truediv__(self, other: Self) -> Vec[float]:
        return Vec(*map(operator.truediv, self, other))

    def __neg__(self) -> Self:
        return type(self)(*map(operator.neg, self))

    def __abs__(self) -> Self:
        return type(self)(*map(abs, self))

    def __getitem__(self, key: int) -> N:
        return self.scalars[key]

    def dot(self, other: Self) -> N:
        return sum(self * other)

    def len(self) -> float:
        return math.sqrt(self.dot(self))

    def __repr__(self) -> str:
        return "<" + ' '.join(map(str, self)) + ">"

class Vec2(Vec[N]):
    def __init__(self, x: N, y: N):
        super(Vec2, self).__init__(x, y)

    def __truediv__(self, other: Self) -> Vec2[float]:
        return Vec2(*super().__truediv__(other).scalars)

    @property
    def x(self) -> N:
        return self.scalars[0]

    @property
    def y(self) -> N:
        return self.scalars[1]

class GridBase(Generic[T]):
    Index = tuple[int, int] | Vec2

    ADJACENT_DIAG = (Vec2(-1, -1), Vec2(-1, 1), Vec2(1, -1), Vec2(1, 1))
    ADJACENT_CROSS = (Vec2(-1, 0), Vec2(0, -1), Vec2(0, 1), Vec2(1, 0))
    ADJACENT = ADJACENT_DIAG + ADJACENT_CROSS

    def __init__(self, data: Sequence[Sequence[T]]):
        if not all(map(lambda row: len(data[0]) == len(row),
                       islice(data, 1, None))):
            raise ValueError

        self.rows = len(data)
        self.cols = len(data[0])
        self.data = data

    @classmethod
    def empty(cls, rows: int, cols: int, filler: T) -> Self:
        data = [[filler for _ in range(cols)] for _ in range(rows)]
        return cls(data)

    @staticmethod
    def _to_vec(idx: Index) -> Vec2:
        if isinstance(idx, tuple):
            assert all(map(lambda x: isinstance(x, int), idx))
            return Vec2(*reversed(idx))
        if isinstance(idx, Vec2):
            return idx
        raise ValueError

    def is_inbounds(self, idx: Index) -> bool:
        v = self._to_vec(idx)
        return 0 <= v.x < self.cols and 0 <= v.y < self.rows

    def _adjacent(self, idx: Index, probes=ADJACENT) -> Iterator[Vec2]:
        v = self._to_vec(idx)
        return filter(self.is_inbounds, map(lambda offs: v + offs, probes))

    adjacent = _adjacent
    adjacent_diag = partialmethod(_adjacent, probes=ADJACENT_DIAG)
    adjacent_cross = partialmethod(_adjacent, probes=ADJACENT_CROSS)

    def dfs(self, at: Index, key=lambda x: True, adj=adjacent) \
            -> Iterator[Vec2]:
        visited = set()
        stack = [self._to_vec(at)]
        while stack:
            vec = stack.pop()
            if self.is_inbounds(vec) and vec not in visited and key(vec):
                visited.add(vec)
                yield vec
                stack.extend(adj(self, vec))

    def bfs(self, at: Index, key=lambda x: True, adj=adjacent) \
            -> Iterator[Vec2]:
        visited = set()
        queue = deque((self._to_vec(at),))
        while queue:
            vec = queue.popleft()
            if self.is_inbounds(vec) and vec not in visited and key(vec):
                visited.add(vec)
                yield vec
                queue.extend(adj(self, vec))

    def get(self, key: Index, default: Optional[T]=None) -> Optional[T]:
        v = self._to_vec(key)
        return self.data[v.y][v.x] if self.is_inbounds(v) else default

    def row(self, idx: int) -> Sequence[T]:
        return self.data[idx]

    def __contains__(self, key: T) -> bool:
        return any(map(lambda row: key in row, self.data))

    def __getitem__(self, key: Index) -> T:
        v = self._to_vec(key)
        return self.data[v.y][v.x]

    def __iter__(self) -> Iterator[Sequence[T]]:
        return iter(self.data)

    def __repr__(self) -> str:
        buf = io.StringIO()
        row_pad = len(str(self.rows - 1))
        col_pad = max(map(lambda row: max(map(len, map(str, row))), self))
        col_pad = max(col_pad, len(str(self.cols - 1))) + 1
        buf.write(' ' * (row_pad + 2))
        for j in range(self.cols):
            buf.write(str(j).rjust(col_pad))
        buf.write('\n')
        buf.write(' ' * row_pad)
        buf.write(" +")
        buf.write('-' * (self.cols * col_pad))
        for i in range(self.rows):
            buf.write('\n')
            buf.write(str(i).rjust(row_pad))
            buf.write(" |")
            for j in range(self.cols):
                buf.write(str(self[i, j]).rjust(col_pad))
        r = buf.getvalue()
        buf.close()
        return r

class Grid(GridBase[T]):
    def __init__(self, data: Sequence[Sequence[T]]):
        super().__init__(data)
        self.repr: Optional[str] = None

    def __hash__(self) -> int:
        h = hash((self.rows, self.cols))
        for row in self.data:
            for col in row:
                h ^= hash(col)
        return h

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Grid):
            raise ValueError
        return self.data == other.data

    def __repr__(self) -> str:
        if self.repr is None:
            self.repr = super().__repr__()
        return self.repr

class MutGrid(GridBase[T]):
    def __init__(self,
                 data: MutableSequence[MutableSequence[T]],
                 pad: Optional[T]=None):
        if pad is not None:
            max_col = max(map(len, data))
            for row in data:
                assert isinstance(row, list)
                for _ in range(len(row) - max_col):
                    row.append(pad)
        super().__init__(data)
        self.mut_data = data

    def copy(self) -> Self:
        return MutGrid(copy.deepcopy(self.mut_data))

    def clear_with(self, val: T):
        for row in self.mut_data:
            for j in range(len(row)):
                row[j] = val

    def __setitem__(self, key: MutGrid.Index, val: T) -> T:
        v = self._to_vec(key)
        self.mut_data[v.y][v.x] = val
        return val

def main():
    #G = Grid(["abcdeeeeee",
    #          "kbcdeeeeee",
    #          "ebcdeeeeee",
    #          "kbcdeeeeee",
    #          "jbcdeeeeee",
    #          "lbcdeeeeee",
    #          "mbcdeeeeee",
    #          "ibcdeeeeee",
    #])
    #G = Grid([(1, 2, 2, 2, 2, 2, 2, 2, 22, 2),
    #          (3, 4, 2, 2, 2, 2, 2, 2, 22, 2)])
    G = Grid([(1, 2, 38732194823),
              (3, 4, 16214323243)])
    print(G,
          [*G.bfs((0, 0))],
          [*G.dfs((0, 0))],
          [*G.adjacent((0, 0))],
          [*G.adjacent_cross((0, 0))],
          [*G.adjacent_diag((0, 0))],
          sep='\n')

if __name__ == "__main__":
    main()
    raise SystemExit
