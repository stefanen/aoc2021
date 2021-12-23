from collections import Counter
from functools import cache
from itertools import combinations, product
from typing import Iterable


def rotations(v: Iterable[int]):
    x, y, z = v
    return [
        (-z, -y, -x),
        (-z, -x, y),
        (-z, x, -y),
        (-z, y, x),
        (-y, -z, x),
        (-y, -x, -z),
        (-y, x, z),
        (-y, z, -x),
        (-x, -z, -y),
        (-x, -y, z),
        (-x, y, -z),
        (-x, z, y),
        (x, -z, y),
        (x, -y, -z),
        (x, y, z),
        (x, z, -y),
        (y, -z, -x),
        (y, -x, z),
        (y, x, -z),
        (y, z, x),
        (z, -y, x),
        (z, -x, -y),
        (z, x, y),
        (z, y, -x),
    ]


def add_vec(p1: Iterable[int], p2: Iterable[int]) -> tuple[int, ...]:
    return tuple(a + b for a, b in zip(p1, p2))


import random


@cache
def sub_vec(p1: Iterable[int], p2: Iterable[int]) -> tuple[int, ...]:
    return tuple(a - b for a, b in zip(p1, p2))


def manhattan(p1: Iterable[int], p2: Iterable[int]) -> int:
    return sum(abs(a - b) for a, b in zip(p1, p2))


shiftlist: list[tuple[int, ...]] = []


def merge_overlap(scan: set[tuple[int, ...]], scanners: list[set[tuple[int, ...]]]):
    random.shuffle(scanners)
    for i, scanner in enumerate(scanners):
        for rotation in zip(*(rotations(v) for v in scanner)):
            c = Counter(sub_vec(a, b) for a, b in product(scan, rotation))
            pos, count = c.most_common(1)[0]
            if count >= 12:
                shiftlist.append(pos)
                scanners.pop(i)
                scanners.append(scan | {add_vec(p, pos) for p in rotation})
                return scanners
    raise ValueError


scans = reversed(open("sample.txt").read().split("\n\n"))
scanners = [{tuple(map(int, a.split(","))) for a in s.splitlines()[1:]} for s in scans]
random.shuffle(scanners)

while len(scanners) > 1:
    scanners = merge_overlap(scanners.pop(), scanners)

# part 1
print(len(scanners[0]))

# part 2
print(max(manhattan(a, b) for a, b in combinations(shiftlist, 2)))
