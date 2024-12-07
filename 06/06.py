from itertools import cycle
from time import time

from rich import print

from grid import Grid, Vector, grid_from_input_txt, NORTH, EAST, SOUTH, WEST


def get_puzzle_input():
    input_filename = "input.txt"
    #input_filename = "example.txt"
    with open(input_filename) as input_txt:
        return grid_from_input_txt(input_txt.read(), "O")

def guard_status(grid:Grid, location, direction, starting_location, starting_direction):
    if grid[location] == "O":
        return "off-grid"
    if location == starting_location and direction == starting_direction:
        return "loop"
    return "live"

def traverse(grid:Grid, mark=None):
    location_direction_seen = set()
    def guard_status(location, direction):
        if grid[location] == "O":
            return "off-grid"
        location_direction = (location, direction)
        if location_direction in location_direction_seen:
            return "loop"
        location_direction_seen.add(location_direction)
        return "live"

    location = grid.find_one("^")
    rotation = cycle([NORTH, EAST, SOUTH, WEST])  # Note, Starting with NORTH
    direction = next(rotation)
    status = "live"
    while status == "live":
        if mark is not None:
            grid[location] = mark
        while grid[location + direction] == "#":
            direction = next(rotation)
            status = guard_status(location, direction)

        location += direction
        status = guard_status(location, direction)

    return status

def solve_part_1(grid: Grid):
    traverse(grid, mark="X")

    print(len(grid.grid))
    return len(list(grid.find("X")))

def solve_part_2(grid:Grid):
    start_time = time()
    loop_count = 0
    for i, modification_location in enumerate(list(grid.find("."))):

        grid[modification_location] = "#"
        status = traverse(grid)
        if status == "loop":
            loop_count += 1
        grid[modification_location] = "."
        if i % 100 == 0:
            print(f"Progress: {i} ({loop_count} found)")

    print(f"Elapsed time: {time() - start_time}")

    return loop_count

if __name__ == "__main__":
    answer_1 = solve_part_1(get_puzzle_input())
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(get_puzzle_input())
    print(f"Part 2: {answer_2}")
