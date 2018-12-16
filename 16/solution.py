def addr(registers, opcode, a, b, c):
    registers[c] = registers[a] + registers[b]


def addi(registers, opcode, a, b, c):
    registers[c] = registers[a] + b


def mulr(registers, opcode, a, b, c):
    registers[c] = registers[a] * registers[b]


def muli(registers, opcode, a, b, c):
    registers[c] = registers[a] * b


def banr(registers, opcode, a, b, c):
    registers[c] = registers[a] & registers[b]


def bani(registers, opcode, a, b, c):
    registers[c] = registers[a] & b


def borr(registers, opcode, a, b, c):
    registers[c] = registers[a] | registers[b]


def bori(registers, opcode, a, b, c):
    registers[c] = registers[a] | b


def setr(registers, opcode, a, b, c):
    registers[c] = registers[a]


def seti(registers, opcode, a, b, c):
    registers[c] = a


def gtir(registers, opcode, a, b, c):
    if a > registers[b]:
        registers[c] = 1
    else:
        registers[c] = 0


def gtri(registers, opcode, a, b, c):
    if registers[a] > b:
        registers[c] = 1
    else:
        registers[c] = 0


def gtrr(registers, opcode, a, b, c):
    if registers[a] > registers[b]:
        registers[c] = 1
    else:
        registers[c] = 0


def eqir(registers, opcode, a, b, c):
    if a == registers[b]:
        registers[c] = 1
    else:
        registers[c] = 0


def eqri(registers, opcode, a, b, c):
    if registers[a] == b:
        registers[c] = 1
    else:
        registers[c] = 0


def eqrr(registers, opcode, a, b, c):
    if registers[a] == registers[b]:
        registers[c] = 1
    else:
        registers[c] = 0


OPCODE_FUNCS = 'addr addi mulr muli banr bani borr bori setr seti gtir gtri gtrr eqir eqri eqrr'.split()


def read():
    samples = []
    program = []

    with open('input.txt', 'r') as fin:
        while True:
            l1 = fin.readline()
            if l1 == '':
                break
            l1 = l1.strip()
            if l1.startswith('Before: '):
                l2 = fin.readline().strip()
                l3 = fin.readline().strip()
                fin.readline()  # blank line
                samples.append((
                    eval(l1[7:]),
                    [int(v) for v in l2.split()],
                    eval(l3[7:]),
                ))
            elif l1 != '':
                program.append([int(v) for v in l1.split()])

    return samples, program


def first(samples):
    total = 0

    for s in samples:
        private_registers = s[0]
        cnt = 0

        for func_name in OPCODE_FUNCS:
            func = globals()[func_name]
            registers = private_registers[:]
            func(registers, *s[1])
            if registers == s[2]:
                cnt += 1

        if cnt >= 3:
            total += 1

    print(total)


def second(samples, program):
    d = {}

    while True:
        if len(d) == len(OPCODE_FUNCS):
            break

        for s in samples:
            private_registers = s[0]
            valid_opcode_funcs = set()

            if d.get(s[1][0]) is not None:
                continue

            unknown_funcs = set(OPCODE_FUNCS) - set(d.values())

            for func_name in unknown_funcs:
                func = globals()[func_name]
                registers = private_registers[:]
                func(registers, *s[1])
                if registers == s[2]:
                    valid_opcode_funcs.add(func_name)

            if len(valid_opcode_funcs) == 1:
                d[s[1][0]] = valid_opcode_funcs.pop()

    registers = [0, 0, 0, 0]
    for statement in program:
        globals()[d[statement[0]]](registers, *statement)

    print(registers[0])


def main():
    samples, program = read()
    first(samples)
    second(samples, program)


if __name__ == '__main__':
    main()
