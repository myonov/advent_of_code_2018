from collections import namedtuple
import re

Point = namedtuple('Point', ['x', 'y', 'dx', 'dy'])


def read():
    def extract(s):
        return [int(v) for v in s.split(', ')]

    r = []
    pattern = 'position=<(?P<point>.*)> velocity=<(?P<vec>.*)>'
    with open('input.txt', 'r') as fin:
        for line in fin:
            matched = re.match(pattern, line)
            args = extract(matched.group('point')) + extract(matched.group('vec'))
            r.append(Point(*args))

    return r


def point_in_time(p, t):
    return p.x + t * p.dx, p.y + t * p.dy


def bounding_box(moving_points, t):
    x, y = point_in_time(moving_points[0], t)
    left, bottom = x, y
    right, top = x, y

    for p in moving_points[1:]:
        x, y = point_in_time(p, t)
        if left > x:
            left = x
        if right < x:
            right = x
        if top > y:
            top = y
        if bottom < y:
            bottom = y

    return top, left, bottom, right


def box_size(b):
    return (b[2] - b[0] + 1) * (b[3] - b[1] + 1)


def box_bigger_or_eq(b1, b2):
    return box_size(b1) >= box_size(b2)


def output(points, t):
    print(t)
    s = {point_in_time(p, t) for p in points}
    box = bounding_box(points, t)
    with open('output.txt', 'w') as fout:
        for y in range(box[0], box[2] + 1):
            for x in range(box[1], box[3] + 1):
                c = '*' if (x, y) in s else '.'
                print(c, end='', file=fout)
            print(file=fout)


def solve(points):
    t = 0
    prev_box = bounding_box(points, t)
    while True:
        t += 1
        box = bounding_box(points, t)
        if box_bigger_or_eq(box, prev_box):
            t -= 1
            break
        prev_box = box
    output(points, t)


def main():
    points = read()
    solve(points)


if __name__ == '__main__':
    main()
