import math
import typing


class Queue:
    def __init__(self, iterable_object: typing.Iterable):
        self.__queue = []
        for obj in iterable_object:
            self.__queue.append(obj)

    def add(self, element):
        self.__queue.insert(0, element)

    def pop(self):
        if not self.is_empty():
            return self.__queue.pop()

    def is_empty(self):
        return not bool(self.__queue)

    def __len__(self):
        return len(self.__queue)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_hit = False

    def is_none(self):
        return self.x is None or self.y is None

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return f'Point: x = {self.x}, y = {self.y}'


class CoordConverter:
    @staticmethod
    def absolute_to_matrix(abs_coord, size):
        y = abs_coord//size
        x = abs_coord - y*size
        return Point(x, y)

    @staticmethod
    def matrix_to_absolute(point: Point, size):
        return point.y*size + point.x


def distance(point1: Point, point2: Point):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)



