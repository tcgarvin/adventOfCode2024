import argparse
import re
import math
from typing import NamedTuple

import numpy as np
from rich import print

# Regex courtesy of chatgpt
PATTERN = re.compile(r"""
Button\s*A:\s*X\+(\d+),\s*Y\+(\d+)\s*
Button\s*B:\s*X\+(\d+),\s*Y\+(\d+)\s*
Prize:\s*X=(\d+),\s*Y=(\d+)
""", re.VERBOSE)

MachineInfo = NamedTuple("MachineInfo", [("ax", int), ("ay", int), ("bx", int), ("by", int), ("px", int), ("py", int)])

def get_puzzle_input(use_example=False):
    input_filename = "example.txt" if use_example else "input.txt"
    puzzle_input = []
    with open(input_filename) as input_txt:
        for match in PATTERN.finditer(input_txt.read()):
            puzzle_input.append(MachineInfo(*map(int, match.groups())))
    return puzzle_input

def cheapest_win(machine: MachineInfo, max_pushes=False, correction=0) -> int:
    px = machine.px + correction
    py = machine.py + correction
    # Ax = b 
    np_A = np.array([[machine.ax, machine.bx], [machine.ay, machine.by]])
    np_b = np.array([px, py])
    raw_solution = np.linalg.solve(np_A, np_b)
    solution = raw_solution.round()

    # Validate solution.  We expect rounding into make bad solutions look checkable, but they should fail.
    a,b = int(solution[0]), int(solution[1])
    cost = 0
    if a < 0 or b < 0:
        cost = 0

    elif max_pushes is not False and (a > max_pushes or b > max_pushes):
        cost = 0

    elif a * machine.ax + b * machine.bx == px and a * machine.ay + b * machine.by == py:
        cost = 3 * a + b

    #print(machine)
    #print(raw_solution, solution, (a,b), cost)
    return cost


def solve_part_1(machines: list[MachineInfo]):
    total_min_cost = 0
    for machine in machines:
        total_min_cost += cheapest_win(machine, max_pushes=100)

    return total_min_cost

def solve_part_2(machines: list[MachineInfo]):
    total_min_cost = 0
    for machine in machines:
        total_min_cost += cheapest_win(machine, correction=10000000000000)

    return total_min_cost

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--example", action="store_true")
    args = parser.parse_args()

    puzzle_input = get_puzzle_input(use_example=args.example)

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")
