import argparse
from functools import reduce
import re
from typing import NamedTuple

from rich import print

from grid import Vector, get_vector, Grid, print_grid

# Regex courtesy of copilot:
# capture the 4 integers from: p=7,38 v=-61,12
ROBOT_RE = re.compile(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)")

# We're going to take Vector.i to be y, and Vector.j to be x.
RobotStart = NamedTuple("RobotStart", [("p", Vector), ("v", Vector)])

def get_puzzle_input(use_example=False):
    input_filename = "example.txt" if use_example else "input.txt"
    puzzle_input = []
    with open(input_filename) as input_txt:
        for line in input_txt:
            if line.startswith("#"):
                width, height = map(int, line[1:].split("x"))
                continue
            match = ROBOT_RE.match(line)
            robot = RobotStart(
                p=get_vector(int(match.group(2)), int(match.group(1))),
                v=get_vector(int(match.group(4)), int(match.group(3))),
            )
            #print(robot)
            puzzle_input.append(robot)
    return (width, height), puzzle_input

def solve_part_1(size:tuple[int, int], robots: list[RobotStart]):
    width, height = size
    quadrant_counts = [0,0,0,0]
    debug_grid = Grid(out_of_bounds="X")
    for i in range(height):
        for j in range(width):
            debug_grid[get_vector(i,j)] = "."

    print_grid(debug_grid)
    for robot in robots:
        end_position_uncorrected = robot.p + robot.v * 100
        end_position = get_vector(end_position_uncorrected.i % height, end_position_uncorrected.j % width)

        if debug_grid[end_position] == ".":
            debug_grid[end_position] = "1"
        else:
            debug_grid[end_position] = str(int(debug_grid[end_position]) + 1)

        print(robot, end_position)

        # Quadrants are:
        # 0 1
        # 2 3

        mid_width = width // 2
        mid_height = height // 2
        print(mid_height, mid_width)

        if end_position.i < mid_height and end_position.j < mid_width:
            quadrant_counts[0] += 1
        elif end_position.i > mid_height and end_position.j < mid_width:
            quadrant_counts[1] += 1
        elif end_position.i < mid_height and end_position.j > mid_width:
            quadrant_counts[2] += 1
        elif end_position.i > mid_height and end_position.j > mid_width:
            quadrant_counts[3] += 1

    print_grid(debug_grid)

    return reduce(lambda a,b: a*b, quadrant_counts)

def solve_part_2(size:tuple[int,int], robots: list[RobotStart]):
    width, height = size

    robot_positions = {r:r.p for r in robots}

    i = 0
    while True:
        debug_grid = Grid(out_of_bounds="X")
        for y in range(height):
            for x in range(width):
                debug_grid[get_vector(y,x)] = "."

        for robot in robots:
            position = robot_positions[robot] + robot.v
            position = get_vector(position.i % height, position.j % width)
            robot_positions[robot] = position

            if debug_grid[position] == ".":
                debug_grid[position] = "1"
            else:
                debug_grid[position] = str(int(debug_grid[position]) + 1)


        i += 1
        if (i - 50) % 103 == 0:
            print_grid(debug_grid)
            print(i)
            input()
        elif (i - 97) % 101 == 0:
            print_grid(debug_grid)
            print(i)
            input()

    return i

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--example", action="store_true")
    args = parser.parse_args()

    size,puzzle_input = get_puzzle_input(use_example=args.example)

    answer_1 = solve_part_1(size, puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(size, puzzle_input)
    print(f"Part 2: {answer_2}")
