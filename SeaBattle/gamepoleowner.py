import random

from utils import Queue, CoordConverter, Point
import GameOptions as options


class GamePoleOwner:
    def __init__(self, gamepole):
        self.gamepole = gamepole

    @property
    def ships(self):
        return self.gamepole.get_ships()

    @property
    def size(self):
        return self.gamepole._size


class ShipsMover(GamePoleOwner):
    def __init__(self, gamepole):
        super().__init__(gamepole)

    def move_all_ships(self, step=1):
        move_queue = Queue(self.ships)

        count = 0
        while move_queue:
            ship_to_move = move_queue.pop()
            if self.move_forward(ship_to_move, step):
                count = 0
            else:
                if self.move_backward(ship_to_move, step):
                    count = 0
                else:
                    move_queue.add(ship_to_move)
                    count += 1

            if count == len(move_queue):
                break

    def move_forward(self, ship, step) -> bool:
        ship.move(step)
        if self.gamepole.is_collision(ship) or ship.is_out_pole(self.size):
            ship.move(-step)
            return False
        return True

    def move_backward(self, ship, step) -> bool:
        return self.move_forward(ship, -step)


class ShipConstellator(GamePoleOwner):
    def __init__(self, gamepole):
        super().__init__(gamepole)
        self.allowed_cells = list(range(self.size * self.size))

    def place_ships(self):
        for ship in self.ships:
            try:
                self.place_ship(ship)
            except ValueError:
                ship.reverse_orientation()
                self.place_ship(ship)

    def place_ship(self, ship):
        ship.orientation = random.choice([options.HORIZONTAL, options.VERTICAL])
        local_allowed_cells = self.allowed_cells.copy()

        while local_allowed_cells:
            position_absolute = random.choice(local_allowed_cells)
            start_point = CoordConverter.absolute_to_matrix(position_absolute, self.size)
            ship.start_point = start_point

            if self.gamepole.is_collision(ship) or ship.is_out_pole(self.size):
                ship.start_point = Point(None, None)
                local_allowed_cells.remove(position_absolute)
            else:
                break

        if ship.start_point.is_none():
            raise ValueError('Не удалось разместить корабль. Попробуйте снова')

        self.exclude_restricted_area_of(ship)

    def exclude_restricted_area_of(self, ship):
        restricted_area = self.gamepole.get_restricted_ship_area(ship)

        for restricted_point in restricted_area:
            abs_cell = CoordConverter.matrix_to_absolute(restricted_point, self.size)

            if abs_cell in self.allowed_cells:
                self.allowed_cells.remove(abs_cell)
