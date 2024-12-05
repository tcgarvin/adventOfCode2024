from rich import print

from grid import (
    grid_from_input_txt,
    Grid,
    ALL_DIRECTION_VECTORS,
    Vector,
    NORTH_EAST,
    NORTH_WEST,
    SOUTH_EAST,
    SOUTH_WEST,
)


def get_puzzle_input():
    puzzle_input = []
    with open("input.txt") as input_txt:
        puzzle_input = grid_from_input_txt(input_txt.read())
    return puzzle_input


def solve_part_1(puzzle_input: Grid):
    xmases_found = 0
    for starting_vector in puzzle_input.all_locations():
        if puzzle_input[starting_vector] != "X":
            continue

        for direction in ALL_DIRECTION_VECTORS:
            found_xmax = True
            for i, character in enumerate("XMAS"):
                if puzzle_input[starting_vector + direction * i] != character:
                    found_xmax = False
                    break

            if found_xmax:
                xmases_found += 1

    return xmases_found


def solve_part_2(puzzle_input: Grid):
    MS = set("MS")
    xmases_found = 1
    for starting_vector in puzzle_input.all_locations():
        if puzzle_input[starting_vector] != "A":
            continue

        northwest_char = puzzle_input[starting_vector + NORTH_WEST]
        southeast_char = puzzle_input[starting_vector + SOUTH_EAST]
        northeast_char = puzzle_input[starting_vector + NORTH_EAST]
        southwest_char = puzzle_input[starting_vector + SOUTH_WEST]

        if (
            set([northwest_char, southeast_char]) == MS
            and set([northeast_char, southwest_char]) == MS
        ):
            xmases_found += 1

    return xmases_found


if __name__ == "__main__":
    puzzle_input = get_puzzle_input()

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")
