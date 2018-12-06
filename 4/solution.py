def minutes(hm):
    return int(hm.split(':')[1])


def main():
    data = []
    with open('input.txt', 'r') as fin:
        for line in fin:
            parts = line.split()
            data.append((parts[0][1:], parts[1][:-1], ' '.join(parts[2:])))
    data.sort()

    guard_data = {}
    for event in data:
        if event[2].startswith('Guard'):
            guard_id = event[2].split()[1][1:]
            guard = guard_data.setdefault(guard_id, {'tot': 0})
        if event[2] == 'falls asleep':
            start = minutes(event[1])
        if event[2] == 'wakes up':
            end = minutes(event[1])
            guard['tot'] += end - start
            for m in range(start, end):
                guard.setdefault(m, 0)
                guard[m] += 1

    best = 0
    for g in guard_data:
        if guard_data[g]['tot'] > best:
            best = guard_data[g]['tot']

    mx = 0
    minute = 0
    gid = None
    best_minute = 0
    best_in_best_minute = 0
    best_gid = 0
    for g in guard_data:
        if guard_data[g]['tot'] == best:
            for m in range(60):
                k = guard_data[g].get(m, 0)
                if k > mx:
                    mx = k
                    minute = m
                    gid = g
        for m in range(60):
            k = guard_data[g].get(m, 0)
            if k > best_in_best_minute:
                best_in_best_minute = k
                best_minute = m
                best_gid = g


    print(minute * int(gid))
    print(best_minute * int(best_gid))


if __name__ == '__main__':
    main()
