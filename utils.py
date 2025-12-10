# Copyright (C) 2025 by pan <pan_@disroot.org>
# SPDX-License-Identifier: 0BSD

from __future__ import annotations

import argparse
import copy
import io
import math
import operator
import re
import sys

from abc import abstractmethod
from collections import deque
from collections.abc import (Callable, Iterator, Iterable, MutableSequence,
                             Sequence)
from dataclasses import dataclass
from enum import Enum
from functools import partial, partialmethod
from itertools import chain, islice
from pathlib import Path
from typing import (Any, Generic, NamedTuple, Optional, Self, TypeVar,
                    NoReturn, TextIO, Protocol, cast)

T = TypeVar("T")
U = TypeVar("U")

frozen = partial(dataclass, frozen=True)


#
# Misc.
#

class UnreachableError(RuntimeError):
    pass

def unreachable(*args, **kwargs) -> NoReturn:  # type: ignore
    print(*args, file=sys.stderr, **kwargs)
    raise UnreachableError

def identity(x: T) -> T:
    return x

def some(opt: Optional[T]) -> T:
    assert opt is not None
    return opt

def swap_pop(L: list[T], idx: int) -> T:
    L[idx], L[-1] = L[-1], L[idx]
    return L.pop()

def trim_newline(itr: Iterator[str]) -> Iterator[str]:
    first: str
    try:
        first = next(itr)
    except StopIteration:
        return
    try:
        while True:
            second = next(itr)
            yield first
            first = second
    except StopIteration:
        if first != "\n":
            yield first

def main(go: Callable[[Iterator[str]], Iterator[Any]],  # type: ignore
         unpack: bool=False,
         string: bool=True,
         strip: bool=True,
         trimnl: bool=True,
         **kwargs) -> None:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("filepath", nargs='?', type=str, default=None)
    if string:
        group.add_argument("-s", "--string", required=False, type=str)
    args = parser.parse_args()

    file: Optional[TextIO]
    itr: Iterator[str]
    if string and args.string is not None:
        file = None
        itr = iter((cast(str, args.string),))
    else:
        filepath = cast(Optional[str], args.filepath)
        file = sys.stdin if filepath is None or filepath == "-" \
               else open(Path(filepath), "r", encoding="utf-8")
        itr = iter(file)

    out = go(map(str.strip if strip else identity,
                 trim_newline(itr) if trimnl else itr))
    if unpack:
        for x in out:
            if type(x) is tuple:
                print(*x, **kwargs)
            else:
                print(x, **kwargs)
    else:
        for x in out:
            print(x, **kwargs)

    if file is not None and file is not sys.stdin:
        file.close()


#
# Iterators.
#

try:
    from itertools import batched as batched
except ImportError:
    def batched(itr: Iterator[T],  # type: ignore[no-redef]
                n: int, *, strict: bool=False) -> Iterator[tuple[T, ...]]:
        # batched("ABCDEFG", 3) -> ABC DEF G
        if n < 1:
            raise ValueError("n must be at least one")
        it = iter(itr)
        while batch := (*islice(it, n),):
            if strict and len(batch) != n:
                raise ValueError("batched(): incomplete batch")
            yield batch

def integers(itr: Iterator[str], signed: bool=True) -> Iterator[int]:
    uint_pat = r"(?:0|[1-9]\d*)"
    pat = fr"(-?{uint_pat})" if signed else fr"({uint_pat})"
    nums = chain.from_iterable(map(lambda s: re.finditer(pat, s), itr))
    return map(lambda match: int(match[0]), nums)

def first(itr: Iterator[T], key=lambda x: True) -> Optional[T]:  # type: ignore
    try:
        return next(filter(key, itr))  # type: ignore
    except StopIteration:
        return None

def last(itr: Iterator[T],
         key: Callable[[T], bool]=lambda x: True) -> Optional[T]:
    r = None
    for x in filter(key, itr):
        r = x
    return r

def take(itr: Iterator[T], n: int, *, strict: bool=False) -> Iterator[T]:
    # take("ABCDEFG",  3) -> ABC
    # take("ABCDEFG",  0) ->
    # take("ABCDEFG", -1) -> ABCDEFG
    if n < -1:
        raise ValueError("n must be int [-1, +inf)")
    if n != 0:
        it = iter(itr)
        for i, x in enumerate(it, start=1):
            yield x
            if i == n:
                break
        if strict and n != -1 and i != n:
            raise ValueError("take(): incomplete iterator")

def ilen(itr: Iterator[T]) -> int:
    i = 0
    for i, _ in enumerate(itr, start=1):
        pass
    return i

def apply(func: Callable[..., T], *iterables) -> None:  # type: ignore
    for args in zip(*iterables):
        func(*args)

def joinlines(itr: Iterator[str], strip: bool=True) -> str:
    return "".join(map(str.strip if strip else identity, itr))

def nth(stream: Sequence[T] | Iterator[T], n: int) -> Optional[T]:
    if isinstance(stream, Sequence):
        return stream[n] if n < len(stream) else None

    for i, x in enumerate(stream):
        if i == n:
            return x
    return None

def empty_iter() -> Iterator[T]:
    yield from ()

class Comparable(Protocol):
    def __lt__(self, other: Self) -> bool: ...
    def __gt__(self, other: Self) -> bool: ...

CT = TypeVar("CT", bound=Comparable)

def ct_identity(x: CT) -> CT:
    return x

def minmax(itr: Iterable[CT], key: Callable[[CT], CT]=ct_identity) \
        -> Optional[tuple[CT, CT]]:
    it = iter(itr)
    minval: CT
    maxval: CT
    try:
        minval = maxval = key(next(it))
    except StopIteration:
        return None
    for x in map(key, it):
        if x < minval:
            minval = x
        if x > maxval:
            maxval = x
    return (minval, maxval)


#
# Debug.
#

class DebugPrint:
    def __init__(self, enabled: bool=True):
        self.enabled = enabled

    def on(self) -> Self:
        self.enabled = True
        return self

    def off(self) -> Self:
        self.enabled = False
        return self

    def toggle(self) -> Self:
        self.enabled ^= True
        return self

    def peek(self, itr: Iterator[T], sep: str=" ", end: str="\n") \
            -> Iterator[T]:
        for x in itr:
            self(x, end=sep)
            yield x
        self(end=end)

    class MapFmt(Enum):
        IN     = 0  # => in
        OUT    = 1  # => out
        IN_OUT = 2  # => in -> out

    def map(self,  # type: ignore
            func: Callable[..., T],
            *iterables,
            sep: str=", ",
            end: str="\n",
            fmt: MapFmt=MapFmt.IN_OUT) -> Iterator[T]:
        pat = ("{0}", "{1}", "{0} -> {1}")[fmt.value]
        for args in zip(*iterables):
            r = func(*args)
            self(pat.format(args if len(args) > 1 else args[0], r), end=sep)
            yield r
        self(end=end)

    def take(self, itr: Iterator[T], sep: str=" ", end: str="\n") -> Self:
        for x in itr:
            self(x, end=sep)
        self(end=end)
        return self

    def identity(self, x: T, end: str ="\n") -> T:
        self(x, end=end)
        return x

    def __call__(self, *args, **kwargs) -> Self:  # type: ignore
        if self.enabled:
            print(*args, **kwargs)
        return self


#
# Geometry.
#

N = TypeVar("N", int, float)

@dataclass(frozen=True)
class Vec(Generic[N]):
    scalars: tuple[N, ...]

    def __init__(self, *args: N):
        object.__setattr__(self, "scalars", args)

    def __iter__(self) -> Iterator[N]:
        return iter(self.scalars)

    def __add__(self, other: Self) -> Self:
        return type(self)(*map(operator.add, self, other))

    def __sub__(self, other: Self) -> Self:
        return type(self)(*map(operator.sub, self, other))

    def __mul__(self, other: N | Self) -> Self:
        cls = type(self)
        if isinstance(other, (int, float)):
            return cls(*map(lambda scalar: scalar * other, self))
        return cls(*map(operator.mul, self, other))

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

    def __lt__(self, other: Self) -> bool:
        return self.scalars < other.scalars

    def __le__(self, other: Self) -> bool:
        return self.scalars <= other.scalars

    def __ge__(self, other: Self) -> bool:
        return self.scalars >= other.scalars

    def __gt__(self, other: Self) -> bool:
        return self.scalars > other.scalars

    def __len__(self) -> int:
        return len(self.scalars)

    def dot(self, other: Self) -> N:
        return sum(self * other)

    def len(self) -> float:
        return math.sqrt(self.dot(self))

    def min(self: Vec[int]) -> Vec[int]:
        gcd = math.gcd(*self)
        return type(self)(*map(lambda scalar: scalar // gcd, self))

    def __repr__(self) -> str:
        return "<" + ' '.join(map(str, self)) + ">"

class Vec2(Vec[N]):
    def __init__(self, x: N=0, y: N=0):
        super(Vec2, self).__init__(x, y)

    def __truediv__(self, other: Self) -> Vec2[float]:
        return Vec2(*super().__truediv__(other).scalars)

    @property
    def x(self) -> N:
        return self.scalars[0]

    @property
    def y(self) -> N:
        return self.scalars[1]

@dataclass(frozen=True)
class Adjacent:
    sym: str
    vec: Vec2[int]

    def __str__(self) -> str:
        return f"{self.sym}:{self.vec}"

class Adjacents(Enum):
    UP_LEFT    = Adjacent('↖', Vec2(-1, -1))
    LEFT       = Adjacent('←', Vec2(-1,  0))
    DOWN_LEFT  = Adjacent('↙', Vec2(-1,  1))
    UP         = Adjacent('↑', Vec2( 0, -1))
    DOWN       = Adjacent('↓', Vec2( 0,  1))
    UP_RIGHT   = Adjacent('↗', Vec2( 1, -1))
    RIGHT      = Adjacent('→', Vec2( 1,  0))
    DOWN_RIGHT = Adjacent('↘', Vec2( 1,  1))

    @property
    def vec(self) -> Vec2[int]:
        return self.value.vec

    def __str__(self) -> str:
        return self.value.sym


#
# Grid.
#

class GridBase(Generic[T]):
    Index = tuple[int, int] | Vec2[int]

    ADJACENT_DIAG  = (*map(lambda adj: adj.value.vec, (Adjacents.UP_LEFT,
                                                       Adjacents.DOWN_LEFT,
                                                       Adjacents.UP_RIGHT,
                                                       Adjacents.DOWN_RIGHT)),)
    ADJACENT_CROSS = (*map(lambda adj: adj.value.vec, (Adjacents.LEFT,
                                                       Adjacents.UP,
                                                       Adjacents.DOWN,
                                                       Adjacents.RIGHT)),)
    ADJACENT = (*map(lambda adj: adj.value.vec, Adjacents),)

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
    def _to_vec(idx: Index) -> Vec2[int]:
        if isinstance(idx, tuple):
            assert all(map(lambda x: isinstance(x, int), idx))
            return Vec2(*reversed(idx))
        if isinstance(idx, Vec2):
            return idx
        raise ValueError

    def is_inbounds(self, idx: Index) -> bool:
        v = self._to_vec(idx)
        return 0 <= v.x < self.cols and 0 <= v.y < self.rows

    def _adjacent(self, idx: Index, probes: tuple[Vec2[int], ...]=ADJACENT) \
            -> Iterator[Vec2[int]]:
        v = self._to_vec(idx)
        return filter(self.is_inbounds, map(lambda offs: v + offs, probes))

    adjacent = _adjacent
    adjacent_diag = partialmethod(_adjacent, probes=ADJACENT_DIAG)
    adjacent_cross = partialmethod(_adjacent, probes=ADJACENT_CROSS)

    def dfs(self,
            at: Index,
            key: Callable[[Vec2[int]], bool]=lambda x: True,
            adj: Optional[Callable[[Index], Iterator[Vec2[int]]]]=None) \
                -> Iterator[Vec2[int]]:
        if adj is None:
            adj = self.adjacent
        visited = set()
        stack = [self._to_vec(at)]
        while stack:
            vec = stack.pop()
            if self.is_inbounds(vec) and vec not in visited:
                visited.add(vec)
                if key(vec):
                    yield vec
                    stack.extend(adj(vec))

    def bfs(self,
            at: Index,
            key: Callable[[Vec2[int]], bool]=lambda x: True,
            adj: Optional[Callable[[Index], Iterator[Vec2[int]]]]=None) \
                -> Iterator[Vec2[int]]:
        if adj is None:
            adj = self.adjacent
        visited = set()
        queue = deque((self._to_vec(at),))
        while queue:
            vec = queue.popleft()
            if self.is_inbounds(vec) and vec not in visited:
                visited.add(vec)
                if key(vec):
                    yield vec
                    queue.extend(adj(vec))

    def get(self, key: Index, default: Optional[T]=None) -> Optional[T]:
        v = self._to_vec(key)
        return self.data[v.y][v.x] if self.is_inbounds(v) else default

    def row(self, idx: int) -> Sequence[T]:
        return self.data[idx]

    def find(self,
             val: T,
             start: Vec2[int]=Vec2(0, 0),
             stop: Vec2[int]=Vec2(-1, -1)) -> Vec2[int]:
        if stop < Vec2(0, 0):
            stop = Vec2(self.cols, self.rows)

        data = self.data
        for i in range(start.y, stop.y):
            j: int
            try:
                j = data[i].index(val, start.x, stop.x)
            except ValueError:
                pass
            else:
                return Vec2(j, i)
        return Vec2(-1, -1)

    def rfind(self,
              val: T,
              start: Vec2[int]=Vec2(0, 0),
              stop: Vec2[int]=Vec2(-1, -1)) -> Vec2[int]:
        if stop < Vec2(0, 0):
            stop = Vec2(self.cols, self.rows)

        r = Vec2(-1, -1)
        data = self.data
        for i in range(start.y, stop.y):
            j: int
            try:
                j = data[i].index(val, start.x, stop.x)
            except ValueError:
                pass
            else:
                r = Vec2(j, i)
        return r

    def count(self, val: T) -> int:
        return sum(map(lambda row: row.count(val), self.data))

    def to_str(self,
               delim: str="",
               rows: bool=False,
               edges: bool=False) -> str:
        buf = io.StringIO()
        row_pad = len(str(self.rows - 1))
        col_pad = max(map(lambda row: max(map(len, map(str, row))), self))
        if edges:
            if rows:
                buf.write(' ' * (row_pad + 1))
            buf.write('+')
            buf.write('-' * (self.cols * col_pad * (len(delim) + 1)))
            buf.write("+\n")
        for i in range(self.rows):
            if i > 0:
                buf.write('\n')
            if rows:
                buf.write(str(i).rjust(row_pad))
                buf.write(' ')
            if edges:
                buf.write('|')
            for j in range(self.cols):
                buf.write(str(self[i, j]).rjust(col_pad))
                buf.write(delim)
            if edges:
                buf.write('|')
        if edges:
            buf.write('\n')
            if rows:
                buf.write(' ' * (row_pad + 1))
            buf.write('+')
            buf.write('-' * (self.cols * col_pad * (len(delim) + 1)))
            buf.write('+')
        r = buf.getvalue()
        buf.close()
        return r

    def __contains__(self, key: T) -> bool:
        return any(map(lambda row: key in row, self.data))

    def __getitem__(self, key: Index) -> T:
        v = self._to_vec(key)
        return self.data[v.y][v.x]

    def __iter__(self) -> Iterator[Sequence[T]]:
        return iter(self.data)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, GridBase):
            raise ValueError
        return self.data == other.data

    def ravel(self) -> Iterator[T]:
        for row in self.data:
            yield from row

    def cords(self) -> Iterator[Vec2[int]]:
        for i in range(self.rows):
            for j in range(self.cols):
                yield Vec2(j, i)

    def pairs(self) -> Iterator[tuple[Vec2[int], T]]:
        for i, row in enumerate(self.data):
            for j, item in enumerate(row):
                yield (Vec2(j, i), item)

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
        self.hash: Optional[int] = None
        self.repr: Optional[str] = None

    def __hash__(self) -> int:
        if self.hash is None:
            h = hash((self.rows, self.cols))
            for row in self.data:
                for col in row:
                    h = hash((h, col))
            self.hash = h
        return self.hash

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
                for _ in range(len(row) - max_col):
                    row.append(pad)
        super().__init__(data)
        self.mut_data = data

    def mut_row(self, idx: int) -> MutableSequence[T]:
        return self.mut_data[idx]

    def copy(self) -> Self:
        return type(self)(copy.deepcopy(self.mut_data))

    def clear_with(self, val: T) -> None:
        for row in self.mut_data:
            for j in range(len(row)):
                row[j] = val

    def __setitem__(self, key: MutGrid.Index, val: T) -> T:
        v = self._to_vec(key)
        self.mut_data[v.y][v.x] = val
        return val


#
# Functional programming.
#

@dataclass(frozen=True)
class Composer[X, Y]:
    f: Callable[[X], Y]

    def __call__[Z](self, g: Callable[[Z], X]) -> Composer[Z, Y]:
        def fog(z: Z) -> Y:
            return self.f(g(z))
        return Composer(fog)

    # Composer(...) << x
    def __lshift__(self, x: X) -> Y:
        return self.f(x)

@dataclass(frozen=True)
class Pipeline[X, Y]:
    f: Callable[[X], Y]

    def __call__[Z](self, g: Callable[[Y], Z]) -> Pipeline[X, Z]:
        def gof(x: X) -> Z:
            return g(self.f(x))
        return Pipeline(gof)

    # x >> Pipeline(...)
    def __rrshift__(self, x: X) -> Y:
        return self.f(x)

# compose(f, g)(x) = f(g(x))
def compose[X, Y, Z](f: Callable[[X], Y], g: Callable[[Z], X]) \
        -> Callable[[Z], Y]:
    return Composer(f)(g).f

# pipe(f, g)(x) = g(f(x))
def pipe[X, Y, Z](f: Callable[[X], Y], g: Callable[[Y], Z]) \
        -> Callable[[X], Z]:
    return Pipeline(f)(g).f


#
# Math
#

def ceildiv(x: int, y: int) -> int:
    return -(x // -y)

def floordiv(x: int, y: int) -> int:
    return x // y

# Same as C's `/`.
def truncdiv(x: int, y :int) -> int:
    return ceildiv(x, y) if (x < 0) != (y < 0) else x // y

# Same as C's `%`.
def remainder(x: int, y: int) -> int:
    return (-1 if x < 0 else 1) * (abs(x) % abs(y))

def euclidiv(x: int, y: int) -> int:
    q = truncdiv(x, y)
    r = remainder(x, y)
    if r < 0:
        if y > 0:
            q -= 1
        else:
            q += 1
    return q

def euclidmod(x: int, y: int) -> int:
    r = remainder(x, y)
    if r < 0:
        if y > 0:
            r += y
        else:
            r -= y
    return r


#
#
#

def test() -> None:
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
          G == G,
          [*G.bfs((0, 0))],
          [*G.dfs((0, 0))],
          [*G.adjacent((0, 0))],
          [*G.adjacent_cross((0, 0))],
          [*G.adjacent_diag((0, 0))],
          sep='\n')

if __name__ == "__main__":
    test()
    raise SystemExit
