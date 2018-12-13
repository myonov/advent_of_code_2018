from collections import namedtuple


Cart = namedtuple('Cart', ['i', 'j', 'dir', 'turn'])
Corner = namedtuple('Corner', ['i', 'j', 'dirs'])
Intersection = namedtuple('Intersection', ['i', 'j'])

DIRECTION = {
    'LEFT': (0, -1),
    'UP': (-1, 0),
    'RIGHT': (0, 1),
    'DOWN': (1, 0),
}
DIRECTION_KEYS = ['LEFT', 'UP', 'RIGHT', 'DOWN']
LEFT = 0
STRAIGHT = 1
RIGHT = 2


def is_corner(c):
    return c == '\\' or c == '/'


def is_cart(c):
    return c in '<>^v'


def is_intersection(c):
    return c == '+'


def make_corner(data, i, j):
    dirs = []

    for k, d in DIRECTION.items():
            ni, nj = i + d[0], j + d[1]
            if k in ('LEFT', 'RIGHT'):
                c = '-<>'
            else:
                c = '|^v'
            try:
                if data[ni][nj] in c or is_intersection(data[ni][nj]):
                    dirs.append(d)
            except IndexError:
                pass

    assert len(dirs) == 2
    return Corner(i, j, tuple(dirs))


def make_cart(data, i, j):
    d = None

    if data[i][j] == '>':
        d = DIRECTION['RIGHT']
    if data[i][j] == '<':
        d = DIRECTION['LEFT']
    if data[i][j] == '^':
        d = DIRECTION['UP']
    if data[i][j] == 'v':
        d = DIRECTION['DOWN']

    assert d is not None
    return Cart(i, j, d, LEFT)


def make_intersection(i, j):
    return Intersection(i, j)


def read():
    carts = []
    corners = {}
    intersections = {}

    with open('input.txt', 'r') as fin:
        data = []
        for line in fin:
            data.append(line.rstrip())

        for i in range(len(data)):
            for j in range(len(data[i])):
                if is_corner(data[i][j]):
                    corners[(i, j)] = make_corner(data, i, j)
                if is_cart(data[i][j]):
                    carts.append(make_cart(data, i, j))
                if is_intersection(data[i][j]):
                    intersections[(i, j)] = make_intersection(i, j)

    return carts, corners, intersections


def next_turn(current_turn):
    return (current_turn + 1) % 3


def move_cart(cart, corners, intersections):
    pos = cart.i + cart.dir[0], cart.j + cart.dir[1]

    if pos in corners:
        c = corners[pos]
        oi, oj = c.i + c.dirs[0][0], c.j + c.dirs[0][1]
        if oi == cart.i and oj == cart.j:
            d = c.dirs[1]
        else:
            d = c.dirs[0]
        return Cart(pos[0], pos[1], d, cart.turn)

    if pos in intersections:
        d = None
        if cart.turn == STRAIGHT:
            d = cart.dir

        ind = None
        for i, k in enumerate(DIRECTION_KEYS):
            if DIRECTION[k] == cart.dir:
                ind = i
                break

        if cart.turn == LEFT:
            # DIRECTION_KEYS are clockwise; left is the previous index
            d = DIRECTION[DIRECTION_KEYS[(ind + 3) % 4]]

        if cart.turn == RIGHT:
            # right is next index
            d = DIRECTION[DIRECTION_KEYS[(ind + 1) % 4]]

        assert d is not None
        return Cart(pos[0], pos[1], d, next_turn(cart.turn))

    return Cart(pos[0], pos[1], cart.dir, cart.turn)


def old_positions(carts):
    return ((c.i, c.j) for c in carts)


def solve(carts, corners, intersections, stop_on_first_crash=False):
    while True:
        carts = sorted(carts)
        positions = {}

        while carts:
            c = carts[0]
            carts = carts[1:]
            new_cart = move_cart(c, corners, intersections)
            pos = new_cart.i, new_cart.j

            if pos in positions or pos in old_positions(carts):
                if stop_on_first_crash:
                    print(pos[1], pos[0])
                    return
                try:
                    del positions[pos]
                except KeyError:
                    pass
                carts = [c for c in carts if (c.i, c.j) != pos]
            else:
                positions[pos] = new_cart

        carts = list(positions.values())
        if len(carts) == 1:
            last = carts[0]
            print(last.j, last.i)
            return


def main():
    carts, corners, intersections = read()
    solve(carts, corners, intersections, True)
    solve(carts, corners, intersections, False)


if __name__ == '__main__':
    main()
