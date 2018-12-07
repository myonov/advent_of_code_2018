import re
from collections import defaultdict


def read_rules():
    g = defaultdict(set)
    d = defaultdict(int)
    with open('input.txt', 'r') as fin:
        for line in fin:
            m = re.match('Step (?P<first>.) must be finished before step (?P<second>.) can begin.', line)
            first, second = m.group('first'), m.group('second')
            g[first].add(second)
            d[first] += 0
            d[second] += 1
    return g, d


def top_sort(graph, _d):
    d = _d.copy()
    mkey = max(d.keys())
    r = []
    while d:
        b = mkey
        for k in d:
            if d[k] == 0 and k <= b:
                b = k
        r.append(b)
        for v in graph[b]:
            d[v] -= 1
        del d[b]
    return ''.join(r)


def first(graph, d):
    print(top_sort(graph, d))


def time_needed(v):
    return ord(v) - ord('A') + 61


def filter_q(q):
    r, other = [], []
    t = min(q)[0]

    for v in q:
        if v[0] == t:
            r.append(v[1])
        else:
            other.append(v)
    return t, r, other


def free_nodes(r, graph, d):
    for v in r:
        for g in graph[v]:
            d[g] -= 1


def second(graph, _d):
    d = _d.copy()
    keys_sorted = sorted(d.keys())
    workers = 5

    q = []
    for k in keys_sorted:
        if d[k] == 0 and len(q) < workers:
            q.append((time_needed(k), k))
            del d[k]

    t = 0
    while q:
        t, nodes_to_advance, q = filter_q(q)
        free_nodes(nodes_to_advance, graph, d)
        for k in keys_sorted:
            if d.get(k) == 0 and len(q) < workers:
                q.append((t + time_needed(k), k))
                del d[k]
    print(t)


def main():
    graph, d = read_rules()
    first(graph, d)
    second(graph, d)


if __name__ == '__main__':
    main()
