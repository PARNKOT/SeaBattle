from itertools import product
from typing import List
from utils import Point, distance
import GameOptions as options


class ShipBase:
    def __init__(self):
        self._start_point = Point(None, None)
        self._orientation = options.HORIZONTAL
        self._length = 1
        self._cells = []
        self.is_move = True


class Ship(ShipBase):
    def __init__(self):
        super().__init__()

    def __repr__(self):
        return f'Ship with {self.length} decks, coords: x = {self.start_point.x}, y = {self.start_point.y}, ' \
               f'id = {id(self)}'

    def __str__(self):
        return f'Ship with {self.length} decks, coords: x = {self.start_point.x}, y = {self.start_point.y}, ' \
               f'id = {id(self)}'

    @property
    def length(self):
        return self._length

    @property
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, value):
        if value in (options.HORIZONTAL, options.VERTICAL):
            self._orientation = value

    @property
    def start_point(self) -> Point:
        return self._start_point

    @start_point.setter
    def start_point(self, point: Point):
        self._start_point = point

    # --------------------------------------------- TO THINK
    def is_placed(self):
        if self.start_point.x is None or self.start_point.y is None:
            return False
        return True
    # --------------------------------------------- TO THINK

    def reverse_orientation(self):
        if self.orientation == options.HORIZONTAL:
            self.orientation = options.VERTICAL
        else:
            self.orientation = options.HORIZONTAL

    def move(self, step):
        if self.is_move:
            if self.orientation == options.HORIZONTAL:
                self.move_x(step)
            else:
                self.move_y(step)

    def move_x(self, dx):
        self.start_point.x += dx

    def move_y(self, dy):
        self.start_point.y += dy

    def is_collide(self, ship):
        if self.is_placed() and ship.is_placed():
            for cell_first_ship, cell_second_ship in product(self.get_all_cells_of_ship(),
                                                             ship.get_all_cells_of_ship()):
                dist_between_cells = distance(cell_first_ship, cell_second_ship)
                if dist_between_cells < options.COLLIDE_DIST:
                    return True
        return False

    def is_out_pole(self, size_of_gamepole):
        for point in self.get_all_cells_of_ship():
            if any([point.x < 0 or point.x >= size_of_gamepole,
                    point.y < 0 or point.y >= size_of_gamepole]):
                return True
        return False

    def get_all_cells_of_ship(self) -> List[Point]:
        out = []
        if self.orientation == options.HORIZONTAL:
            for step in range(self.length):
                out.append(Point(self.start_point.x + step, self.start_point.y))
        else:
            for step in range(self.length):
                out.append(Point(self.start_point.x, self.start_point.y + step))
        return out

    def destroy_deck_on(self, point: Point):
        for index, cell in enumerate(self.get_all_cells_of_ship()):
            if cell == point:
                self._cells[index] = options.DESTROYED_CELL
                break

    def is_destroyed(self):
        return all(self._cells)


class OneDeckShip(Ship):
    def __init__(self):
        super().__init__()
        self._length = 1
        self._cells = [0]


class TwoDeckShip(Ship):
    def __init__(self):
        super().__init__()
        self._length = 2
        self._cells = [0, 0]


class ThreeDeckShip(Ship):
    def __init__(self):
        super().__init__()
        self._length = 3
        self._cells = [0, 0, 0]


class FourDeckShip(Ship):
    def __init__(self):
        super().__init__()
        self._length = 4
        self._cells = [0, 0, 0, 0]


if __name__ == "__main__":
    ship = TwoDeckShip()
    ship._cells[0] = options.DESTROYED_CELL
    ship._cells[1] = options.DESTROYED_CELL
    print(ship.is_destroyed())
