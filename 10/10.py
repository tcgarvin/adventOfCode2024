import argparse
from rich import print

from grid import Grid, Vector, grid_from_input_txt, NORTH, EAST, SOUTH, WEST

def get_puzzle_input(use_example=False):
    input_filename = "example.txt" if use_example else "input.txt"
    puzzle_input = None
    with open(input_filename) as input_txt:
        puzzle_input = grid_from_input_txt(input_txt.read(), "!")
    return puzzle_input

def solve_part_1(grid:Grid):
    trailheads = list(grid.find("0"))
    total_score = 0
    for trailhead in trailheads:
        summits = set()
        checked = set()
        to_check = [(trailhead, -1)]
        while len(to_check) > 0:
            location, prior_elevation = to_check.pop(0)
            if grid[location] == "!":
                continue

            elevation = int(grid[location])
            if elevation != prior_elevation + 1:
                continue

            if elevation == 9:
                summits.add(location)
                continue

            for direction in [NORTH, EAST, SOUTH, WEST]:
                new_location = location + direction
                if new_location in checked:
                    continue
                to_check.append((new_location, elevation))

            checked.add(location)
        
        score = len(summits)
        total_score += score

    return total_score

def get_trailhead_rating(grid:Grid, location:Vector):
    elevation = int(grid[location])
    if elevation == 9:
        return 1

    rating = 0
    for direction in (NORTH, EAST, SOUTH, WEST):
        new_location = location + direction
        if grid[new_location] == "!":
            continue

        if int(grid[new_location]) == elevation + 1:
            rating += get_trailhead_rating(grid, new_location)

    return rating


def solve_part_2(grid:Grid):
    trailheads = list(puzzle_input.find("0"))
    total_score = 0
    for trailhead in trailheads:
        total_score += get_trailhead_rating(grid, trailhead)

    return total_score

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--example", action="store_true")
    args = parser.parse_args()

    puzzle_input = get_puzzle_input(use_example=args.example)

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")
