class Node:
    def __init__(self, val):
        self.val = val
        self.prev = None
        self.next = None


def print_list(node, iterations):
    for _ in range(iterations):
        print(node.val, end=' ')
        node = node.next
    print()


def game(num_players, last_marble):
    scores = [0 for _ in range(num_players)]

    n = Node(0)
    n.prev = n
    n.next = n
    curr = n
    current_player = 0

    for i in range(1, last_marble+1):
        current_player = (current_player + 1) % num_players
        if i % 23 == 0:
            scores[current_player] += i
            for _ in range(8):
                curr = curr.prev
            scores[current_player] += curr.next.val
            curr.next = curr.next.next
            curr.next.prev = curr.prev.prev
            curr = curr.next
        else:
            insert_after = curr.next
            node = Node(i)
            node.next = insert_after.next
            insert_after.next.prev = node
            insert_after.next = node
            node.prev = insert_after
            curr = node

    return max(scores)


def first():
    print(game(459, 71320))


def second():
    print(game(459, 7132000))


def main():
    first()
    second()


if __name__ == '__main__':
    main()
