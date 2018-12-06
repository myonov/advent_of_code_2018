import random
from collections import namedtuple, Counter

Point = namedtuple('Point', ['x', 'y'])
INF = 10 ** 15
COEF = [-10, 0, 10]
DISTANCE_LIMIT = 10000


def read():
    points = []
    with open('input.txt', 'r') as fin:
        for line in fin:
            points.append(Point(*[int(x) for x in line.strip().split(', ')]))
    return points


def get_bounding_box(points):
    top, bottom = -INF, INF
    right, left = -INF, INF

    for p in points:
        right = max(p.x, right)
        left = min(p.x, left)
        top = max(p.y, top)
        bottom = min(p.y, bottom)

    return Point(left, bottom), Point(right, top)


def distance(p1, p2):
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)


def closest(p, points):
    if not points:
        return set()

    c = {points[0]}
    best = distance(p, points[0])

    for other in points:
        k = distance(p, other)
        if k == best:
            c.add(other)
        if k < best:
            best = k
            c = {other}

    if len(c) > 1:
        return set()

    return c


def get_inner_points(points, bounding_box):
    inner = set(points)
    iterations = 100000

    width = bounding_box[1].x - bounding_box[0].x
    height = bounding_box[1].y - bounding_box[0].y

    for _ in range(iterations):
        x = random.randint(bounding_box[0].x, bounding_box[1].x)
        y = random.randint(bounding_box[0].y, bounding_box[1].y)

        for coef_x in COEF:
            for coef_y in COEF:
                if coef_x == 0 and coef_y == 0:
                    continue
                nx = x + coef_x * width
                ny = y + coef_y * height
                inner -= closest(Point(nx, ny), points)

    return inner


def largest(points, inner_points, bounding_box):
    d = Counter()
    for x in range(bounding_box[0].x, bounding_box[1].x + 1):
        for y in range(bounding_box[0].y, bounding_box[1].y + 1):
            c = closest(Point(x, y), points)
            if len(c) == 1 and c & inner_points:
                d[c.pop()] += 1
    return d.most_common(1)[0]


def first(points, bounding_box):
    inner_points = get_inner_points(points, bounding_box)
    print(largest(points, inner_points, bounding_box))


def second(points, bounding_box):
    width = bounding_box[1].x - bounding_box[0].x
    height = bounding_box[1].y - bounding_box[0].y

    cnt = 0
    for x in range(bounding_box[0].x - width, bounding_box[1].x + width + 1):
        for y in range(bounding_box[0].y - height, bounding_box[1].y + height + 1):
            s = 0
            c = Point(x, y)
            for p in points:
                s += distance(c, p)
            if s < DISTANCE_LIMIT:
                cnt += 1
    print(cnt)


def main():
    points = read()
    bounding_box = get_bounding_box(points)
    first(points, bounding_box)
    second(points, bounding_box)


if __name__ == '__main__':
    main()
