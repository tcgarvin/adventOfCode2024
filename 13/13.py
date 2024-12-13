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

def solve_part_1(machines: list[MachineInfo]):
    for machine in machines:
        print(machine)
    return ""

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
