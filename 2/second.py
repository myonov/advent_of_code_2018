with open('input.txt', 'r') as fin:
    s = [line for line in fin]
    for a in s:
        for b in s:
            cnt = 0
            q = None
            for i, (c1, c2) in enumerate(zip(a, b)):
                if c1 != c2:
                    cnt += 1
                    q = i
            if cnt == 1:
                print(a[:q] + a[q+1:])
