from collections import namedtuple
from functools import cache
from typing import Iterable


class Vector(namedtuple("Vector", ["i", "j"])):
    """
    2D vector.  Since we're usually coming from an ascii grid, we'll say i is
    the row and j  is the column.   0,0 would be the upper left, or the very
    first character.
    """

    def __add__(self, other: "Vector"):
        # Could almost certainly optimize this
        return get_vector(self.i + other.i, self.j + other.j)

    def __mul__(self, other: int):
        """
        Scalar multiplication, not dot product.
        """
        return get_vector(self.i * other, self.j * other)


@cache
def get_vector(i: int, j: int) -> Vector:
    return Vector(i, j)


NORTH = get_vector(-1, 0)
NORTH_EAST = get_vector(-1, 1)
EAST = get_vector(0, 1)
SOUTH_EAST = get_vector(1, 1)
SOUTH = get_vector(1, 0)
SOUTH_WEST = get_vector(1, -1)
WEST = get_vector(0, -1)
NORTH_WEST = get_vector(-1, -1)

ALL_DIRECTION_VECTORS = [
    NORTH,
    NORTH_EAST,
    EAST,
    SOUTH_EAST,
    SOUTH,
    SOUTH_WEST,
    WEST,
    NORTH_WEST,
]


class Grid:
    """
    2D Grid. Not sure this shouldn't just be defaultdict like I usually do.
    """

    def __init__(self, out_of_bounds="."):
        self.grid = {}
        self.out_of_bounds = out_of_bounds

    def __getitem__(self, key: Vector):
        return self.grid.get(key, self.out_of_bounds)

    def __setitem__(self, key: Vector, value):
        self.grid[key] = value

    def all_locations(self) -> Iterable[Vector]:
        return self.grid.keys()

    def find(self, value) -> Iterable[Vector]:
        return (location for location, cell in self.grid.items() if cell == value)

    def find_one(self, value) -> Vector:
        found_locations = list(self.find(value))
        assert len(found_locations) == 1
        return found_locations[0]


def grid_from_input_txt(ascii_grid: str, out_of_bounds=".") -> Grid:
    """
    Import an ascii grid into a Grid object
    """
    grid = Grid(out_of_bounds)
    for i, row in enumerate(ascii_grid.split("\n")):
        for j, cell in enumerate(row):
            grid.grid[get_vector(i, j)] = cell
    return grid
