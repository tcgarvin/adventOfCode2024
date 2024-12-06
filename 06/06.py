from itertools import cycle
from rich import print

from grid import Grid, Vector, grid_from_input_txt, NORTH, EAST, SOUTH, WEST


def get_puzzle_input():
    with open("input.txt") as input_txt:
        return grid_from_input_txt(input_txt.read(), "O")

def guard_status(grid:Grid, location, direction, starting_location, starting_direction):
    if grid[location] == "O":
        return "off-grid"
    if location == starting_location and direction == starting_direction:
        return "loop"
    return "live"

def traverse(grid:Grid, mark=None):
    starting_location = grid.find_one("^")
    rotation = cycle([NORTH, EAST, SOUTH, WEST])  # Note, Starting with NORTH
    starting_direction = next(rotation)

    location = starting_location
    direction = starting_direction
    status = "live"
    while status == "live":
        if mark is not None:
            grid[location] = mark
        if grid[location + direction] == "#":
            direction = next(rotation)
            status = guard_status(grid, location, direction, starting_location, starting_direction)

        location += direction
        status = guard_status(grid, location, direction, starting_location, starting_direction)

    return status

def solve_part_1(grid: Grid):
    traverse(grid, mark="X")

    print(len(grid.grid))
    return len(list(grid.find("X")))

def solve_part_2(grid:Grid):

    return ""

if __name__ == "__main__":
    answer_1 = solve_part_1(get_puzzle_input())
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(get_puzzle_input())
    print(f"Part 2: {answer_2}")
