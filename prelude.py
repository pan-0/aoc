# Copyright (C) 2025 by pan <pan_@disroot.org>
# SPDX-License-Identifier: 0BSD

import copy
import heapq
import operator
import re
import string
import sys
import utils

from collections import defaultdict, deque, Counter
from collections.abc import Callable, Iterator, Sequence
from dataclasses import dataclass, field
from enum import Enum, auto
from functools import cache, cmp_to_key, partial, reduce
from io import StringIO
from itertools import (chain, combinations, dropwhile, islice, pairwise,
                       product, permutations, repeat, starmap, takewhile,
                       zip_longest, filterfalse)
from math import prod, sqrt, gcd, lcm
from types import EllipsisType
from typing import Any, NamedTuple, Optional, TypeAlias, cast
from utils import (Adjacents, batched, take, ilen, integers, ceildiv, first,
                   last, apply, identity, joinlines, frozen, Pair, empty_iter)

Input: TypeAlias = Iterator[str]

