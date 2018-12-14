def generate(d, p1, p2):
    c = d[p1] + d[p2]
    d1 = c % 10
    d2 = c // 10
    if d2 > 0:
        d.append(d2)
    d.append(d1)
    p1 = (p1 + d[p1] + 1) % len(d)
    p2 = (p2 + d[p2] + 1) % len(d)
    return p1, p2


def first():
    d = [3, 7]
    limit = 635041
    p1, p2 = 0, 1

    while len(d) < limit + 10:
        p1, p2 = generate(d, p1, p2)

    print(''.join(str(c) for c in d[limit:limit+10]))


def second():
    pattern = [6, 3, 5, 0, 4, 1]

    d = [3, 7]
    p1, p2 = 0, 1

    while True:
        p1, p2 = generate(d, p1, p2)
        for i in range(max(len(d) - 2*len(pattern), 0), max(len(d)-len(pattern)-1, 0)):
            if d[i:i+len(pattern)] == pattern:
                print(i)
                return


def main():
    first()
    second()


if __name__ == '__main__':
    main()
