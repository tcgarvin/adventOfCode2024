from itertools import cycle
from rich import print

from grid import Grid, Vector, grid_from_input_txt, NORTH, EAST, SOUTH, WEST


def get_puzzle_input():
    with open("input.txt") as input_txt:
        return grid_from_input_txt(input_txt.read(), "O")

def solve_part_1(grid: Grid):
    location = puzzle_input.find_one("^")
    rotation = cycle([NORTH, EAST, SOUTH, WEST])  # Note, Starting with NORTH
    direction = next(rotation)
    while grid[location] != "O":
        grid[location] = "X"
        while grid[location + direction] == "#":
            direction = next(rotation)
        location += direction

    return len(list(grid.find("X")))

def solve_part_2(puzzle_input):
    return ""

if __name__ == "__main__":
    puzzle_input = get_puzzle_input()

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")
