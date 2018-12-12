INF = 10 ** 18


def read():
    rules = {}

    with open('input.txt', 'r') as fin:
        raw_initial = fin.readline()
        initial = ''.join([c for c in raw_initial if c in '.#'])

        for line in fin:
            if line.strip() == '':
                continue
            rule, new = line.split('=>')
            rules[rule.strip()] = new.strip()

    return initial, rules


def generate(current, rules, start, end, delta):
    new = {}
    for i in range(start - delta, end + delta):
        s = ''.join(current.get(i + j, '.') for j in range(-2, 3))
        new[i] = rules[s]
    return new


def sum_final(current):
    s = 0

    for i in current:
        if current[i] == '#':
            s += i

    return s


def first(initial, rules):
    iterations = 20
    current = dict(enumerate(initial))
    start, end, delta = 0, len(initial), 3

    for _ in range(iterations):
        new = generate(current, rules, start, end, delta)
        start -= delta
        end += delta
        current = new

    print(sum_final(current))


def extract(generation):
    start, end = INF, -INF

    for i in generation:
        if generation[i] == '#':
            start = min(start, i)
            end = max(end, i)

    r = []
    for i in range(start, end + 1):
        r.append(generation[i])

    return start, ''.join(r)


def second(initial, rules):
    limit = 500000000000
    iteration = 0
    current = dict(enumerate(initial))
    start, end, delta = 0, len(initial), 3
    patterns = {}
    generated = [initial]
    cycle = []

    while True:
        iteration += 1
        new = generate(current, rules, start, end, delta)
        start -= delta
        end += delta
        extract_start, extracted = extract(new)
        if extracted in patterns:
            start_iteration, pos_offset = patterns[extracted]
            for it in range(start_iteration, iteration):
                cycle.append(generated[it])
            offset = extract_start - pos_offset
            break
        current = new
        generated.append(extracted)
        patterns[extracted] = iteration, extract_start

    limit -= patterns[extracted][0] - 1
    start_offset = patterns[extracted][1] - 1 + (limit // len(cycle) - 1) * offset
    limit -= (limit // len(cycle) - 1)

    last = {}
    for i in range(len(cycle[0])):
        last[i + start_offset] = cycle[0][i]
    start, end = start_offset, start_offset + len(cycle[0])

    while limit:
        new = generate(last, rules, start, end, delta)
        start -= delta
        end += delta
        last = new
        limit -= 1

    print(sum_final(last))


def main():
    initial, rules = read()
    first(initial, rules)
    second(initial, rules)


if __name__ == '__main__':
    main()
