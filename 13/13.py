import argparse
import re
from typing import NamedTuple
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

def cheapest_win(machine: MachineInfo) -> int:
    success_pairs = []
    for a_pushes in range(0, 101):
        for b_pushes in range(0, 101):
            if (
                a_pushes * machine.ax + b_pushes * machine.bx == machine.px 
                and a_pushes * machine.ay + b_pushes * machine.by == machine.py
            ):
                success_pairs.append((a_pushes, b_pushes))

    if len(success_pairs) == 0:
        return 0

    cheapest_win = 400 # 100 * 3 + 100 * 1
    for a_pushes, b_pushes in success_pairs:
        cheapest_win = min(cheapest_win, a_pushes * 3 + b_pushes)

    return cheapest_win


def solve_part_1(machines: list[MachineInfo]):
    total_min_cost = 0
    for machine in machines:
        total_min_cost += cheapest_win(machine)

    return total_min_cost

def solve_part_2(puzzle_input):
    return ""

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--example", action="store_true")
    args = parser.parse_args()

    puzzle_input = get_puzzle_input(use_example=args.example)

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")
