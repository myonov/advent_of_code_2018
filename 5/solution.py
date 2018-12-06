from collections import deque


def react(data):
    c = deque()
    for d in data:
        if c and c[-1] != d and c[-1].lower() == d.lower():
            c.pop()
        else:
            c.append(d)
    return len(c)


def main():
    with open('input.txt', 'r') as fin:
        data = fin.read().strip()
    print(react(data))

    best = len(data)
    for i in range(26):
        c_small = chr(ord('a') + i)
        c_big = chr(ord('A') + i)
        r = data.replace(c_small, '').replace(c_big, '')
        k = react(r)
        if k < best:
            best = k
    print(best)


if __name__ == '__main__':
    main()
