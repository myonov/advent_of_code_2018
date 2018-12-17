import sys


def extract(p):
    r = p.split('=')
    r[0] = r[0].strip()
    r[1] = [int(v) for v in r[1].strip().split('..')]
    return r


class WaterSim:
    SINK_COORDS = (500, 0)

    def __init__(self):
        self.walls = set()
        self.water_cells = set()
        self.dropping_water_cells = set()
        self.trapped = set()
        self.sinks = set()
        self.miny = None
        self.maxy = None

    def read(self, filename):
        self.miny, self.maxy = None, None

        with open(filename, 'r') as fin:
            for line in fin:
                info = {}
                info.update(extract(p) for p in line.strip().split(','))
                for x in range(info['x'][0], info['x'][-1] + 1):
                    for y in range(info['y'][0], info['y'][-1] + 1):
                        if self.miny is None or self.miny > y:
                            self.miny = y
                        if self.maxy is None or self.maxy < y:
                            self.maxy = y
                        self.walls.add((x, y))

    def add_water_cell(self, x, y):
        if self.miny <= y <= self.maxy:
            self.water_cells.add((x, y))

    def add_dropping_water_cell(self, x, y):
        if self.miny <= y <= self.maxy:
            self.dropping_water_cells.add((x, y))

    def spread_horizontally(self, x, y, deltax):
        nx = x

        while True:
            p = (nx, y)
            down = (nx, y + 1)

            if p in self.walls:
                return nx - deltax, False

            if down not in self.walls and down not in self.water_cells:
                return nx, True

            self.add_water_cell(nx, y)
            nx += deltax

    def drop_water(self, x, y):
        ny = y

        while ny <= self.maxy and (x, ny) not in self.walls:
            self.add_dropping_water_cell(x, ny)
            ny += 1

        if (x, ny) not in self.walls:
            # below our last layer
            return

        ny -= 1
        nx = x

        while True:
            lx, is_left_opened = self.spread_horizontally(nx, ny, -1)
            rx, is_right_opened = self.spread_horizontally(nx, ny, 1)
            if is_left_opened or is_right_opened:
                break
            for trapped_x in range(lx, rx+1):
                self.trapped.add((trapped_x, ny))
            ny -= 1

        if is_left_opened and not (lx, ny) in self.sinks:
            self.sinks.add((lx, ny))
            self.drop_water(lx, ny)

        if is_right_opened and not (rx, ny) in self.sinks:
            self.sinks.add((rx, ny))
            self.drop_water(rx, ny)

    def visualize(self, fout=sys.stdout):
        minx, maxx = None, None

        for x, y in self.walls:
            if minx is None or minx > x:
                minx = x
            if maxx is None or maxx < x:
                maxx = x

        for y in range(0, self.maxy+5):
            for x in range(minx-5, maxx+5):
                if (x, y) in self.walls:
                    print('#', end='', file=fout)
                elif (x, y) in self.water_cells:
                    print('~', end='', file=fout)
                elif (x, y) in self.dropping_water_cells:
                    print('|', end='', file=fout)
                else:
                    print('.', end='', file=fout)
            print(file=fout)

    def simulate(self):
        self.sinks.add(self.SINK_COORDS)
        self.drop_water(*self.SINK_COORDS)
        with open('debug.txt', 'w') as fout:
            self.visualize(fout)
        print(len(self.water_cells | self.dropping_water_cells))
        print(len(self.trapped))


def main():
    w = WaterSim()
    w.read('input.txt')
    w.simulate()


if __name__ == '__main__':
    main()
