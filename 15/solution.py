import sys
from collections import deque
from copy import deepcopy

INF = 10 ** 18


class Character:
    MAX_HP = 200
    ATTACK_POWER = 3

    def __init__(self, i, j, t, hp=MAX_HP, enemy_power=ATTACK_POWER):
        self.i = i
        self.j = j
        self.t = t
        self.hp = hp
        self.enemy_power = enemy_power
        self.enemy_type = ({'E', 'G'} - {self.t}).pop()

    def move(self, ni, nj):
        self.i = ni
        self.j = nj

    def attack(self):
        self.hp -= self.enemy_power

    def is_dead(self):
        return self.hp <= 0

    def __repr__(self):
        return 'Character({}, {}, \'{}\', {})'.format(self.i, self.j, self.t, self.hp)


class CharacterManager:
    def __init__(self, d=None):
        self.characters = {}
        self.keys_by_type = {}
        self.id = 0
        self.elves_count = 0

        if d is not None:
            self.characters.update(d)
            self.id = max(d) + 1
            self._populate_keys()

    def _populate_keys(self):
        for k, v in self.characters.items():
            self.keys_by_type.setdefault(k, set()).add(k)
        self.elves_count = len(self.keys_by_type.get('E', []))

    def add(self, c):
        self.id += 1
        self.characters[self.id] = c
        self.keys_by_type.setdefault(c.t, set()).add(self.id)
        self.elves_count += c.t == 'E'

    def get(self, c_id, default=None):
        return self.characters.get(c_id, default)

    def of_type(self, t):
        return self.keys_by_type[t]

    def order(self):
        return sorted(self.characters.keys(),
                      key=lambda k: (self.characters[k].i, self.characters[k].j))

    def character_at_position(self, i, j):
        for v in self.characters.values():
            if v.i == i and v.j == j:
                return v
        return None

    def enemies_dead(self):
        for v in self.keys_by_type.values():
            if not v:
                return True
        return False

    def attack(self, enemy_key):
        c = self.characters[enemy_key]
        c.attack()
        if c.is_dead():
            del self.characters[enemy_key]
            self.keys_by_type[c.t].remove(enemy_key)

    def has_enemy_near(self, attacker, attacking_positions):
        b = None
        r_id = None

        for i, j, enemy_id in attacking_positions:
            e = self.characters[enemy_id]
            if attacker.i == i and attacker.j == j:
                if b is None or b.hp > e.hp or b.hp == e.hp and (b.i, b.j) > (e.i, e.j):
                    b = e
                    r_id = enemy_id

        return r_id

    def score(self):
        s = 0

        for c in self.characters.values():
            s += c.hp

        return s

    def increase_gnome_enemy_attack(self, enemy_power):
        for k in self.keys_by_type['G']:
            self.characters[k].enemy_power = enemy_power

    def __repr__(self):
        return 'CharacterManager({})'.format(self.characters)


class DeadEnemiesException(Exception):
    pass


class Map:
    def __init__(self):
        self.m = []
        self.characters = CharacterManager()

    def read(self, filename):
        with open(filename, 'r') as fin:
            for i, line in enumerate(fin):
                row = []
                for j, c in enumerate(line.strip()):
                    if c in 'EG':
                        self.characters.add(Character(i, j, c))
                        c = '.'
                    row.append(c)
                self.m.append(row)

    @property
    def width(self):
        return len(self.m[0])

    @property
    def height(self):
        return len(self.m)

    def in_bounds(self, i, j):
        return 0 <= i < self.height and 0 <= j <= self.width

    def empty(self, i, j):
        return self.m[i][j] == '.'

    def path_restore(self, start_pos, end_pos, d, prev):
        if end_pos == start_pos:
            yield prev

        for ni, nj in self.neighbours(*end_pos):
            if d.get((ni, nj)) == d[end_pos] - 1:
                yield from self.path_restore(start_pos, (ni, nj), d, end_pos)

    def neighbours(self, i, j):
        delta = [(-1, 0), (0, 1), (1, 0), (0, -1)]

        for d in delta:
            ni = i + d[0]
            nj = j + d[1]

            if self.in_bounds(ni, nj) and self.empty(ni, nj):
                yield (ni, nj)

    def get_attacking_positions(self, enemy_type):
        r = []
        enemy_keys = self.characters.of_type(enemy_type)

        for k in enemy_keys:
            e = self.characters.get(k)
            if e is None:
                continue
            for ni, nj in self.neighbours(e.i, e.j):
                c = self.characters.character_at_position(ni, nj)
                if c is None or c.t != enemy_type:
                    r.append((ni, nj, k))

        return r

    def step(self, c, attacking_positions):
        d = {(c.i, c.j): 0}
        q = deque([(c.i, c.j)])

        while q:
            i, j = q.popleft()
            for pos in self.neighbours(i, j):
                char = self.characters.character_at_position(*pos)
                if char is None and d.get(pos) is None:
                    d[pos] = d[(i, j)] + 1
                    q.append(pos)

        b = INF
        pos = None
        for i, j, e_key in attacking_positions:
            v = d.get((i, j), INF)
            if v < b:
                b = v
                pos = (i, j, e_key)
            if v != INF and v == b and (i, j) < (pos[0], pos[1]):
                pos = (i, j, e_key)

        if pos is None:
            return None, None

        next_step = min(self.path_restore((c.i, c.j), (pos[0], pos[1]), d, (pos[0], pos[1])))
        c.move(*next_step)
        if d[(pos[0], pos[1])] == 1:
            return True, pos[2]

        return True, None

    def iterate(self):
        for character_id in self.characters.order():
            c = self.characters.get(character_id)
            if c is None:
                # Character has died; skip it
                continue
            enemy_keys = self.characters.of_type(c.enemy_type)
            if len(enemy_keys) == 0:
                raise DeadEnemiesException()
            attacking_positions = self.get_attacking_positions(c.enemy_type)

            d = self.characters.has_enemy_near(c, attacking_positions)
            if d is not None:
                self.characters.attack(d)
                continue

            r, e = self.step(c, attacking_positions)
            if not e:
                continue
            self.characters.attack(e)

    def dead_elves(self):
        return len(self.characters.of_type('E')) < self.characters.elves_count

    def visualize(self, rounds, file=sys.stdout):
        print('After {} rounds:'.format(rounds), file=file)
        d = []
        for i in range(self.height):
            r = []
            for j in range(self.width):
                r.append(self.m[i][j])
            d.append(r)

        for c in self.characters.characters.values():
            d[c.i][c.j] = c.t

        for i in range(self.height):
            print(''.join(d[i]), end='  ', file=file)
            r = []
            for c in self.characters.characters.values():
                if c.i == i:
                    r.append((c.j, c))
            r.sort()
            for q, c in r:
                print('{}({}), '.format(c.t, c.hp), end='', file=file)
            print(file=file)

        print(file=file)


def read():
    m = Map()
    m.read('input.txt')
    return m


def first(m):
    rounds = 0

    with open('debug.txt', 'w') as fout:
        while True:
            m.visualize(rounds, fout)
            try:
                m.iterate()
            except DeadEnemiesException:
                break
            rounds += 1
        m.visualize(rounds, fout)

    print(rounds, m.characters.score(), m.characters.score() * rounds)


def are_elves_alive(m, enemy_power, fout):
    rounds = 0

    m.characters.increase_gnome_enemy_attack(enemy_power)
    # print('Attack level: {}'.format(enemy_power), file=fout)
    while True:
        # m.visualize(rounds, file=fout)
        try:
            m.iterate()
            if m.dead_elves():
                return False, None
        except DeadEnemiesException:
            break
        rounds += 1
    # m.visualize(rounds, fout)
    # print('-' * 30, file=fout)

    return True, rounds * m.characters.score()


def second(m):
    r = (4, 100)
    delta = 100

    with open('debug2.txt', 'w') as fout:
        while True:
            for a in range(*r):
                c = deepcopy(m)
                result, score = are_elves_alive(c, a, fout)
                if result:
                    print(score)
                    return
            r = (r[1], r[1] + delta)


def main():
    m = read()
    first(deepcopy(m))
    second(m)


if __name__ == '__main__':
    main()
