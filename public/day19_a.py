from collections import Counter
from functools import cache
from itertools import permutations, product
from typing import Iterable


def make_rotations(v: Iterable[int]):
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


def add_vec(p1: Iterable[int], p2: Iterable[int]):
    return tuple(a + b for a, b in zip(p1, p2))


@cache
def sub_vec(p1: Iterable[int], p2: Iterable[int]):
    return tuple(a - b for a, b in zip(p1, p2))


def manhattan(p1: Iterable[int], p2: Iterable[int]):
    return sum(abs(a - b) for a, b in zip(p1, p2))


shiftlist = []


def find_overlap(scnr: set[tuple[int, ...]], scannerlist: list[set[tuple[int, ...]]]):
    for i, scanner in enumerate(scannerlist):
        for rot in zip(*(make_rotations(v) for v in scanner)):
            c = Counter(sub_vec(p1, p2) for p1, p2 in product(scnr, rot))
            if (loc := c.most_common(1)[0])[1] >= 12:
                shiftby = loc[0]
                shiftlist.append(shiftby)
                scannerlist.pop(i)
                return [scnr | {add_vec(p, shiftby) for p in rot}] + scannerlist
    raise ValueError


scans = open("sample.txt").read().split("\n\n")
scanners = [{tuple(map(int, a.split(","))) for a in s.splitlines()[1:]} for s in scans]

while len(scanners) > 1:
    scanners = find_overlap(scanners[0], scanners[1:])

print(len(scanners[0]))
print(max(manhattan(a, b) for a, b in permutations(shiftlist, 2)))
