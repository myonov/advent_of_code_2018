s = 0
with open('input.txt', 'r') as fin:
    for line in fin:
        s += int(line)
print(s)