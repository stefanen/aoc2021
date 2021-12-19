import itertools
import time
from collections import Counter
from math import ceil, floor, sqrt

# xmin = 277
# xmax = 318
# ymin = -92
# ymax = -53
xmin = 117
xmax = 7310
ymin = -9546
ymax = -89

xmin = 288
xmax = 330
ymin = -96
ymax = -50

ymin=282184
xmax=482382
ymin=-502273
ymax=-374688


start = time.perf_counter()

print(ymin * (ymin + 1) // 2)


def get_y_t(y, v0):
    return (sqrt((2 * v0 + 1) ** 2 - 8 * y) + 2 * v0 + 1) / 2


def y_ts(ymin: int, ymax: int):
    all_t = Counter[tuple[int, int]]()
    for v in range(ymin, -ymin + 1):
        a, b = get_y_t(ymin, v), get_y_t(ymax, v)
        tmin, tmax = ceil(min(a, b)), floor(max(a, b))
        if tmin <= tmax:
            all_t[(tmin, tmax)] += 1
    return all_t


yt = y_ts(ymin, ymax)
max_t = max(t[1] for t in yt)


def x_ts(xmin: int, xmax: int, max_t: int):
    all_t = Counter[tuple[int, int]]()
    for v in range(1, xmax + 1):
        p = 0
        tmin = 0
        tmax = 0
        for t in range(1, max_t + 1):
            p += v
            v += (0 > v) - (0 < v)
            if xmin <= p <= xmax:
                if not tmin:
                    tmin = t
                tmax = max_t if v == 0 else t
            if v == 0:
                break
            if p > xmax:
                break
        if tmin:
            all_t[(tmin, tmax)] += 1
    return all_t


xt = x_ts(xmin, xmax, max_t)
print(xt)
print(
    sum(yt[ty] * xt[tx] for tx in xt for ty in yt if tx[1] >= ty[0] and ty[1] >= tx[0])
)

print(time.perf_counter() - start)
