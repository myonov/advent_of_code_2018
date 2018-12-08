from collections import deque


class Node:
    def __init__(self, children_count, data_count):
        self.children_count = children_count
        self.data_count = data_count
        self.children = []
        self.data = []

    @classmethod
    def deserialize(cls, data):
        cc, dc = data.popleft(), data.popleft()
        n = Node(cc, dc)
        for i in range(cc):
            n.children.append(cls.deserialize(data))
        for i in range(dc):
            n.data.append(data.popleft())
        return n

    def sum_metadata(self):
        return sum(c.sum_metadata() for c in self.children) + sum(self.data)

    def value(self):
        if not self.children:
            return sum(self.data)

        s = 0
        l = len(self.children)
        for d in self.data:
            if d <= l:
                s += self.children[d - 1].value()

        return s


def read_tree():
    with open('input.txt', 'r') as fin:
        data = deque(int(v) for v in fin.read().strip().split())
    return Node.deserialize(data)


def first(root):
    print(root.sum_metadata())


def second(root):
    print(root.value())


def main():
    root = read_tree()
    first(root)
    second(root)


if __name__ == '__main__':
    main()
