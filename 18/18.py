import argparse
from heapq import heappop, heappush
from math import inf
from rich import print

from grid import Grid, Vector, get_vector, print_grid, CARDINAL_DIRECTIONS

def get_puzzle_input(use_example=False):
    input_filename = "example.txt" if use_example else "input.txt"
    puzzle_input = []
    with open(input_filename) as input_txt:
        for line in input_txt:
            x,y = tuple(map(int, line.strip().split(",")))
            # We've been using i,j as in row, column, so we'll switch the input
            puzzle_input.append(Vector(y,x))
    return puzzle_input

def solve(puzzle_input:list[Vector]):
    grid = Grid(out_of_bounds="#")
    for x in range(71):
        for y in range(71):
            grid[get_vector(y, x)] = "."
    for location in puzzle_input:
        grid[location] = "#"

    #print_grid(grid)

    # Copy pasta from day 16
    start_location = get_vector(0, 0)
    end_location = get_vector(70, 70)
    to_explore = [(0, start_location)]
    cost_map = {}
    best_cost = inf
    while len(to_explore) > 0:
        cost, location = heappop(to_explore)
        if cost > best_cost:
            break

        if location == end_location:
            best_cost = cost

        if location in cost_map and cost_map[location] <= cost:
            continue

        cost_map[location] = cost

        # Forward
        for direction in CARDINAL_DIRECTIONS:    
            step_location = location + direction
            if grid[step_location] != "#":
                heappush(to_explore, (cost + 1, step_location))

    #print_grid(grid)

    return best_cost, grid

def solve_part_1(puzzle_input):
    return solve(puzzle_input[:1024])

def solve_part_2(puzzle_input):
    at_least = 0
    below = len(puzzle_input)

    final_grid = None
    while below - at_least > 1:
        cursor = at_least + (below - at_least) // 2
        partial_case = puzzle_input[:cursor + 1]
        best_cost, grid = solve(partial_case)
        print(f"Cost of {best_cost} at {cursor}, {puzzle_input[cursor]} {partial_case[-1]}")
        if best_cost == inf:
            below = cursor
        else:
            final_grid = grid
            at_least = cursor

    result = puzzle_input[below]
    final_grid[result] = "X"
    print_grid(final_grid)
    print(at_least, below)

    return f"{result.j},{result.i}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--example", action="store_true")
    args = parser.parse_args()

    puzzle_input = get_puzzle_input(use_example=args.example)

    answer_1, _ = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")
