from typing import List, Set

import GameOptions as options
from ship import (
        Ship,
        OneDeckShip,
        TwoDeckShip,
        ThreeDeckShip,
        FourDeckShip,
    )
from gamepoleowner import ShipsMover, ShipConstellator
from utils import Point


class GamePole:
    __slots__ = ('_size', '_ships', '__allowed_cells', '__pole', 'ships_mover', 'ships_constelattor')

    def __init__(self, size):
        self._size = size
        self._ships: List[Ship] = []
        self.__pole = [[0 for _ in range(size)] for _ in range(size)]
        self.ships_mover = ShipsMover(self)

    def init(self):
        self._ships.clear()
        ships = [
            [OneDeckShip() for _ in range(options.ONE_DECKS)],
            [TwoDeckShip() for _ in range(options.TWO_DECKS)],
            [ThreeDeckShip() for _ in range(options.THREE_DECKS)],
            [FourDeckShip() for _ in range(options.FOUR_DECKS)],
        ]
        for ship_type in ships:
            self._ships.extend(ship_type)

        ShipConstellator(self).place_ships()

    def move_ships(self):
        self.ships_mover.move_all_ships()

    def get_ships(self):
        return self._ships

    def is_collision(self, ship):
        collision = False
        for other_ship in self._ships:
            if id(ship) != id(other_ship):
                collision = ship.is_collide(other_ship)
                if collision:
                    break
        return collision

    def get_cell_neighbours(self, point: Point) -> List[Point]:
        neighbours = []
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                x = point.x + dx
                y = point.y + dy
                if 0 <= x < self._size and 0 <= y < self._size:
                    neighbours.append(Point(x, y))
        return neighbours

    def get_restricted_ship_area(self, ship) -> Set[Point]:
        restricted_cells = set()
        for point in ship.get_all_cells_of_ship():
            neighbours = self.get_cell_neighbours(point)
            restricted_cells.update(neighbours)
        return restricted_cells

    def hit(self, point: Point):
        for ship in self._ships:
            if point in ship.get_all_cells_of_ship():
                ship.destroy_deck_on(point)
                ship.is_move = False
                break
        print(f'Hit on {point}')


if __name__ == "__main__":
    gp = GamePole(10)
    for c in range(1000):
        try:
            gp.init()
        finally:
            print(c)
