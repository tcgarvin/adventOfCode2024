import argparse
import re
import math
from typing import NamedTuple
from rich import print

from grid import Vector

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
    # Kinda outside the scope of the vector class, but should be fine.
    a = Vector(machine.ax, machine.ay)
    b = Vector(machine.bx, machine.by)
    p = Vector(machine.px, machine.py)

    # Hypothesis: The "cheapest", really just means the only, so long as A and B are not scalar multiples of eachother.
    for i in range(10):
        if a * i == b or b * i == a:
            print(f"{machine} has scalar multiple buttons.")

    # We're going to try to change the basis of the coordinate system so that p is defined in terms of A and B.
    # 1. Get the unit vector of A.
    print(f"A: {a}")
    print(f"B: {b}")
    print(f"P: {p}")
    a_unit = a.unit()
    print(f"a_unit: {a_unit}")

    # 2. Get the projection of b onto a.
    b_dot_a = Vector.dot(b, a_unit)
    print(f"b_dot_a: {b_dot_a}")
    b_onto_a = a_unit * b_dot_a
    print(f"b_onto_a: {b_onto_a}")

    # 3. Get B_orthogonal, and its unit.  I feel like I could take a shortcut
    # here, just by using the unit vector of A and taking an educated guess on
    # whether to be right-handed or left-handed, but this feels slightly more
    # scientific.
    b_orth = b - b_onto_a
    b_unit = b_orth.unit()
    print(f"b_unit: {b_unit}")

    # 4. Get the projection of p onto a and b.
    p_onto_a = Vector.dot(p, a_unit)
    p_onto_b = Vector.dot(p, b_unit)
    print(f"p_onto_a: {p_onto_a}")
    print(f"p_onto_b: {p_onto_b}")
    new_p = Vector(p_onto_a, p_onto_b)
    print(f"new_p: {new_p}")

    #5. Let's see if we can get the coordinates of p in terms of a and b.
    a_count = p.i / abs(a)
    b_count = p.j / abs(b)

    print(f"a_count: {a_count}, b_count: {b_count}")

    if a_count < 0 or b_count < 0:
        print(f"{machine} has no solution.")
        return 0

    for a_i in range(math.floor(a_count), math.ceil(a_count) + 1):
        for b_i in range(math.floor(b_count), math.ceil(b_count) + 1):
            if a * a_i + b * b_i == p:
                print(f"{machine} has solution: {a_i}, {b_i}")
                return 3 * a_i + b_i

    print(f"{machine} has no solution.")
    return 0


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
