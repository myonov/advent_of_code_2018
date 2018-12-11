from functools import partial
from multiprocessing.pool import Pool

SIZE = 300
INF = 10 ** 18


def compute(x, y, serial):
    rack_id = x + 10
    power_level = (rack_id * y + serial) * rack_id
    return (power_level // 100) % 10 - 5


def sum_matrix(x, y, r, size):
    s = 0
    for i in range(size):
        for j in range(size):
            s += r[x + i - 1][y + j - 1]
    return s


def compute_r(serial):
    r = [[0 for _ in range(SIZE)] for _ in range(SIZE)]

    for x in range(1, SIZE + 1):
        for y in range(1, SIZE + 1):
            r[x - 1][y - 1] = compute(x, y, serial)

    return r


def find_square(sz, r):
    best = -INF
    coordinates = None

    for x in range(1, SIZE + 1 - sz):
        for y in range(1, SIZE + 1 - sz):
            k = sum_matrix(x, y, r, sz)
            if k > best:
                best = k
                coordinates = (x, y, sz)

    return best, coordinates


def first(r):
    print(find_square(3, r)[1])


def second(r):
    p = Pool(processes=8)
    print(max(p.map(partial(find_square, r=r), range(1, SIZE+1)))[1])


def main():
    r = compute_r(5235)
    first(r)
    second(r)


if __name__ == '__main__':
    main()
