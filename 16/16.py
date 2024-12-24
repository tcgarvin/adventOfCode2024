import argparse
from heapq import heappop, heappush
from math import inf
from typing import NamedTuple
from rich import print

from grid import Grid, grid_from_input_txt, NORTH, EAST, SOUTH, WEST, Vector, print_grid, turn_left, turn_right 

def get_puzzle_input(use_example=False):
    input_filename = "example.txt" if use_example else "input.txt"
    puzzle_input = None
    with open(input_filename) as input_txt:
        puzzle_input = grid_from_input_txt(input_txt.read())
    return puzzle_input

Position = NamedTuple("Position", location=Vector, direction=Vector)

def solve_part_1(grid:Grid):
    start_location = grid.find_one("S")
    end_location = grid.find_one("E")

    start_position = Position(start_location, EAST)
    to_explore = [(0, start_position, None)]
    cost_map = {}
    source_map = {}
    best_cost = inf
    while True:
        cost, position, previous_position = heappop(to_explore)
        if cost > best_cost:
            break

        if position.location == end_location:
            best_cost = cost

        if position in cost_map and cost_map[position] < cost:
            continue

        if previous_position is not None and position in source_map:
            source_map[position].add(previous_position)
        elif previous_position is not None:
            source_map[position] = set([previous_position])

        if position in cost_map and cost_map[position] == cost:
            continue

        cost_map[position] = cost

        # Forward
        step_position = Position(position.location + position.direction, position.direction)
        if grid[step_position.location] != "#":
            heappush(to_explore, (cost + 1, step_position, position))

        # Left
        step_position = Position(position.location, turn_left(position.direction))
        if grid[step_position.location + step_position.direction] != "#":
            heappush(to_explore, (cost + 1000, step_position, position))

        # Right
        step_position = Position(position.location, turn_right(position.direction))
        if grid[step_position.location + step_position.direction] != "#":
            heappush(to_explore, (cost + 1000, step_position, position))

    to_trace = set()
    for end_direction in [NORTH, EAST, SOUTH, WEST]:
        end_position = Position(end_location, end_direction)
        if cost_map.get(end_position, inf) == best_cost:
            to_trace.add(end_position)

    best_path_locations = set()
    while len(to_trace) > 0:
        position = to_trace.pop()
        best_path_locations.add(position.location)
        if position in source_map:
            for source_position in source_map[position]:
                to_trace.add(source_position)

    for location in best_path_locations:
        grid[location] = "O"

    print_grid(grid)

    return best_cost, len(best_path_locations)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--example", action="store_true")
    args = parser.parse_args()

    puzzle_input = get_puzzle_input(use_example=args.example)

    answer_1, answer_2 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")
    print(f"Part 2: {answer_2}")
