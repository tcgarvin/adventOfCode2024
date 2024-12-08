import argparse
from itertools import permutations
import math

from rich import print

from grid import Grid, Vector, grid_from_input_txt, get_vector

ANTENNA = "abcdefghijklmnopqrstuvwxyz"
ANTENNA += ANTENNA.upper()
ANTENNA += "0123456789"

def get_puzzle_input(use_example=False):
    input_filename = "example.txt" if use_example else "input.txt"
    puzzle_input = None
    with open(input_filename) as input_txt:
        puzzle_input = grid_from_input_txt(input_txt.read(), "!")
    return puzzle_input



def solve_part_1(grid:Grid):
    antinode_grid = Grid()
    for char in ANTENNA:
        antenna_locations = list(grid.find(char))
        for l1, l2 in permutations(antenna_locations, 2):
            antinode_location = l2 + (l2 - l1)
            if grid[antinode_location] != "!":
                antinode_grid[antinode_location] = "#"

    return len(list(antinode_grid.find("#")))

def solve_part_2(grid):
    antinode_grid = Grid()
    for char in ANTENNA:
        antenna_locations = list(grid.find(char))
        for l1, l2 in permutations(antenna_locations, 2):

            # This factorization thing appears not to be needed, leaving for completeness
            antenna_difference = l2 - l1 
            resonance_factor = math.gcd(antenna_difference.i, antenna_difference.j)
            resonance_vector = get_vector(antenna_difference.i // resonance_factor, antenna_difference.j // resonance_factor)

            if resonance_vector != antenna_difference:
                print(f"{resonance_vector} {antenna_difference}")
            
            resonance_instance = 0
            out_of_bounds = False
            while not out_of_bounds:
                antinode_location = l1 + resonance_vector * resonance_instance
                if grid[antinode_location] != "!":
                    antinode_grid[antinode_location] = "#"
                else:
                    out_of_bounds = True
                resonance_instance += 1

    return len(list(antinode_grid.find("#")))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--example", action="store_true")
    args = parser.parse_args()

    puzzle_input = get_puzzle_input(use_example=args.example)

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")
