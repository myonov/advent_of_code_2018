from collections import Counter

GROUND = '.'
TREE = '|'
LUMBER = '#'


def read():
    data = []

    with open('input.txt', 'r') as fin:
        for line in fin:
            data.append(line.strip())

    return data


def collect(data, x, y):
    r = Counter()

    for deltax in [-1, 0, 1]:
        for deltay in [-1, 0, 1]:
            if (deltax, deltay) == (0, 0):
                continue

            x1, y1 = x + deltax, y + deltay
            if 0 <= x1 < len(data) and 0 <= y1 < len(data):
                r[data[x1][y1]] += 1

    return r


def iterate(data):
    r = []

    for i in range(len(data)):
        row = []
        for j in range(len(data[i])):
            d = collect(data, i, j)
            if data[i][j] == GROUND:
                row.append(TREE if d[TREE] >= 3 else GROUND)
            elif data[i][j] == TREE:
                row.append(LUMBER if d[LUMBER] >= 3 else TREE)
            else:
                row.append(LUMBER if d[LUMBER] >= 1 and d[TREE] >= 1 else GROUND)
        r.append(''.join(row))

    return r


def score(data):
    c = Counter()
    for i in range(len(data)):
        for j in range(len(data[i])):
            c[data[i][j]] += 1

    return c[TREE] * c[LUMBER]


def first(data):
    iterations = 10

    for _ in range(iterations):
        data = iterate(data)

    print(score(data))


def make_hash(data):
    return ''.join(data)


def second(data):
    limit = 1000000000
    d = {}
    index = {}
    iteration = 0

    while True:
        h = make_hash(data)
        if h in d:
            break
        d[make_hash(data)] = iteration
        index[iteration] = data
        iteration += 1
        data = iterate(data)

    # iteration is bigger than d[h]
    print(score(index[d[h] + (limit - iteration) % (iteration - d[h])]))


def main():
    data = read()
    first(data)
    second(data)


if __name__ == '__main__':
    main()
