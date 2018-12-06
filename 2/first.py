from collections import Counter

with open('input.txt', 'r') as fin:
    twos, threes = 0, 0
    for line in fin:
        c = Counter(line)
        a, b = 0, 0
        for v in c:
            if c[v] == 2:
                a = 1
            if c[v] == 3:
                b = 1
        twos += a
        threes += b
print(twos * threes)