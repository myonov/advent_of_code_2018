from collections import namedtuple

Instruction = namedtuple('Instruction', ['command', 'args'])


class Processor:
    def __init__(self):
        self.registers = [0] * 6
        self.instructions = []
        self.jmp_register = None

    def addr(self, a, b, c):
        self.registers[c] = self.registers[a] + self.registers[b]

    def addi(self, a, b, c):
        self.registers[c] = self.registers[a] + b

    def mulr(self, a, b, c):
        self.registers[c] = self.registers[a] * self.registers[b]

    def muli(self, a, b, c):
        self.registers[c] = self.registers[a] * b

    def banr(self, a, b, c):
        self.registers[c] = self.registers[a] & self.registers[b]

    def bani(self, a, b, c):
        self.registers[c] = self.registers[a] & b

    def borr(self, a, b, c):
        self.registers[c] = self.registers[a] | self.registers[b]

    def bori(self, a, b, c):
        self.registers[c] = self.registers[a] | b

    def setr(self, a, b, c):
        self.registers[c] = self.registers[a]

    def seti(self, a, b, c):
        self.registers[c] = a

    def gtir(self, a, b, c):
        self.registers[c] = 1 if a > self.registers[b] else 0

    def gtri(self, a, b, c):
        self.registers[c] = 1 if self.registers[a] > b else 0

    def gtrr(self, a, b, c):
        self.registers[c] = 1 if self.registers[a] > self.registers[b] else 0

    def eqir(self, a, b, c):
        self.registers[c] = 1 if a == self.registers[b] else 0

    def eqri(self, a, b, c):
        self.registers[c] = 1 if self.registers[a] == b else 0

    def eqrr(self, a, b, c):
        self.registers[c] = 1 if self.registers[a] == self.registers[b] else 0

    @classmethod
    def read(cls, filename):
        processor = Processor()
        with open(filename, 'r') as fin:
            for line in fin:
                if line.startswith('#ip'):
                    processor.jmp_register = int(line.strip().split(' ')[1])
                else:
                    command_with_args = line.strip().split()
                    command = command_with_args[0]
                    args = [int(v) for v in command_with_args[1:]]
                    processor.instructions.append(Instruction(command, args))
        return processor

    @property
    def instruction_pointer(self):
        return self.registers[self.jmp_register]

    @instruction_pointer.setter
    def instruction_pointer(self, val):
        self.registers[self.jmp_register] = val

    def process(self, debug_fout=None):
        steps = 100
        while len(self.instructions) > self.instruction_pointer:
            if steps == 0:
                break
            steps -= 1
            if debug_fout:
                print(self.instruction_pointer, self.registers, file=debug_fout)
            instruction = self.instructions[self.instruction_pointer]
            command = getattr(self, instruction.command)
            command(*instruction.args)
            self.instruction_pointer += 1


def first():
    p = Processor.read('input.txt')
    p.process()
    print(p.registers[0])


def second():
    p = Processor.read('input.txt')
    p.registers = [4, 10, 3, 0, 10551416, 10551417]
    p.registers = [4, 10551416, 3, 0, 9, 10551417]
    # p.registers = [4, 10551416, 3, 0, 8, 10551417]
    # p.registers = [4, 10551416, 3, 0, 7, 10551417]
    # p.registers = [4, 11, 11, 0, 6, 10551417]
    with open('debug2.txt', 'w') as fout:
        p.process(fout)
    print(p.registers[0])


def main():
    # first()
    second()


if __name__ == '__main__':
    main()
