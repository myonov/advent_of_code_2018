s = 0
f = {0}
with open('input.txt', 'r') as fin:
    d = [int(line) for line in fin]
    q = True
    while q:
        for item in d:
            s += item
            if s in f:
                print(s)
                q = False
                break
            f.add(s)
