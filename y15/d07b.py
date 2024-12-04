# SPDX-License-Identifier: 0BSD
# Copyright (C) 2024 by pan <pan_@disroot.org>

from __future__ import annotations

import fileinput
from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import cache, partial
from operator import and_, or_, lshift, rshift

Value = int

class Expr(ABC):
    @abstractmethod
    def eval(self, ctx: Context) -> Value: ...

class Context:
    def __init__(self, syms: dict[str, Expr]):
        self.syms = syms

    @cache
    def eval(self, name: str) -> Value:
        return self.syms[name].eval(self)

    def clear(self):
        self.eval.cache_clear()

    def __setitem__(self, sym: str, expr: Expr):
        self.syms[sym] = expr

frozen = partial(dataclass, frozen=True)

@frozen
class Num(Expr):
    val: Value

    def eval(self, ctx: Context) -> Value:
        return self.val

@frozen
class Id(Expr):
    name: str

    def eval(self, ctx: Context) -> Value:
        return ctx.eval(self.name)

@frozen
class Not(Expr):
    term: Expr

    def eval(self, ctx: Context) -> Value:
        return 0xFFFFFFFF ^ self.term.eval(ctx)

@frozen
class Bin:
    left: Expr
    right: Expr

def bin_eval(op):
    def f(self: Bin, ctx: Context) -> Value:
        return op(self.left.eval(ctx), self.right.eval(ctx))
    return f

@frozen
class And(Expr, Bin):
    eval = bin_eval(and_)

@frozen
class Or(Expr, Bin):
    eval = bin_eval(or_)

@frozen
class Shl(Expr, Bin):
    eval = bin_eval(lshift)

@frozen
class Shr(Expr, Bin):
    eval = bin_eval(rshift)

def term(s: str) -> Expr:
    return Num(Value(s)) if s.isdigit() else Id(s)

def parse(s: str) -> tuple[str, Expr]:
    parts = s.strip().split(' ')
    if parts[0] == "NOT":
        return (parts[3], Not(term(parts[1])))

    op = (
        And if parts[1] == "AND"    else
        Or  if parts[1] == "OR"     else
        Shl if parts[1] == "LSHIFT" else
        Shr if parts[1] == "RSHIFT" else
        None
    )
    if op is None:
        return (parts[2], term(parts[0]))

    left = term(parts[0])
    right = term(parts[2])
    return (parts[4], op(left, right))

def main():
    ctx = Context(dict(map(parse, fileinput.input())))
    a = ctx.eval("a")
    ctx.clear()
    ctx["b"] = Num(a)
    r = ctx.eval("a")
    print(r)

if __name__ == "__main__":
    main()
    raise SystemExit