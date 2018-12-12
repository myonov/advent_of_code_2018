def first():
    initial = '#.......##.###.#.#..##..##..#.#.###..###..##.#.#..##....#####..##.#.....########....#....##.#..##...'
    d = {}
    for i in range(2000):
        d[i] = '.'
        d[-i] = '.'

    for i in range(len(initial)):
        d[i] = initial[i]

    rules = {
        '.....': '.',
        '#....': '.',
        '..###': '.',
        '##..#': '#',
        '.###.': '#',
        '...##': '.',
        '#.#..': '.',
        '..##.': '.',
        '##.#.': '#',
        '..#..': '.',
        '.#...': '#',
        '##.##': '.',
        '....#': '.',
        '.#.#.': '.',
        '#..#.': '#',
        '#.###': '.',
        '.##.#': '#',
        '.####': '.',
        '.#..#': '.',
        '####.': '#',
        '#...#': '#',
        '.#.##': '#',
        '#..##': '.',
        '..#.#': '#',
        '#.##.': '.',
        '###..': '.',
        '#####': '#',
        '###.#': '#',
        '...#.': '#',
        '#.#.#': '#',
        '.##..': '.',
        '##...': '#',
    }

    for _ in range(300):
        new = {}
        for i in range(-2000, 5000):
            c = []
            for k in range(5):
                c.append(d.get(i+k, '.'))
            new[i+2] = rules[''.join(c)]
        d = new

    s = 0
    for i in d:
        if d[i] == '#':
            s += i

    print(s)


def second():
    initial = '#.......##.###.#.#..##..##..#.#.###..###..##.#.#..##....#####..##.#.....########....#....##.#..##...'
    d = {}
    for i in range(2000):
        d[i] = '.'
        d[-i] = '.'

    for i in range(len(initial)):
        d[i] = initial[i]

    rules = {
        '.....': '.',
        '#....': '.',
        '..###': '.',
        '##..#': '#',
        '.###.': '#',
        '...##': '.',
        '#.#..': '.',
        '..##.': '.',
        '##.#.': '#',
        '..#..': '.',
        '.#...': '#',
        '##.##': '.',
        '....#': '.',
        '.#.#.': '.',
        '#..#.': '#',
        '#.###': '.',
        '.##.#': '#',
        '.####': '.',
        '.#..#': '.',
        '####.': '#',
        '#...#': '#',
        '.#.##': '#',
        '#..##': '.',
        '..#.#': '#',
        '#.##.': '.',
        '###..': '.',
        '#####': '#',
        '###.#': '#',
        '...#.': '#',
        '#.#.#': '#',
        '.##..': '.',
        '##...': '#',
    }

    l = {}
    f = None

    for iteration in range(1, 500):
        new = {}
        for i in range(-2000, 2000):
            c = []
            for k in range(5):
                c.append(d.get(i+k, '.'))
            new[i+2] = rules[''.join(c)]
        d = new

        start, end = 2000, -2000
        for i in range(-2000, 2000):
            if d.get(i, '.') == '#':
                start = min(start, i)
                end = max(end, i)
        q = []
        for i in range(start, end + 1):
            q.append(d[i])
        q = ''.join(q)
        if f == q:
            print(q)
            print(iteration)
            break
        if q in l:
            f = q
            print(q)
            print(iteration)
        l[q] = start

    c = 50000000000 - iteration
    # c = 300 - iteration
    offset = l[q]
    print(iteration, offset)

    s = 0
    for i in range(len(q)):
        if q[i] == '#':
            s += (i+1) + offset + c

    print(s)
    # print(l)

    s = 0
    for i in d:
        if d[i] == '#':
            s += i

    # print(s)


def main():
    first()
    second()


if __name__ == '__main__':
    main()
