import argparse
from functools import cache
from itertools import permutations
from math import inf
from rich import print

from grid import (
    Grid,
    Vector,
    get_vector,
    NORTH,
    SOUTH,
    EAST,
    WEST,
    grid_from_input_txt,
    print_grid,
)


def get_puzzle_input(use_example=False):
    input_filename = "example.txt" if use_example else "input.txt"
    puzzle_input = []
    with open(input_filename) as input_txt:
        for line in input_txt:
            puzzle_input.append(line.strip())
    return puzzle_input


def get_keypad() -> Grid:
    grid_txt = "\n".join(["789", "456", "123", " 0A"])
    keypad = grid_from_input_txt(grid_txt)
    keypad.traverse_order = [NORTH, EAST, SOUTH, WEST]
    return keypad


def get_remote_control() -> Grid:
    grid_txt = "\n".join([" ^A", "<v>"])
    remote_control = grid_from_input_txt(grid_txt)
    remote_control.traverse_order = [SOUTH, EAST, NORTH, WEST]
    return remote_control


def is_manhattan_component(component: Vector, whole: Vector):
    # Assumes component is a unit vector north south east or west
    return (
        component.j > 0
        and whole.j > 0
        or component.j < 0
        and whole.j < 0
        or component.i > 0
        and whole.i > 0
        or component.i < 0
        and whole.i < 0
    )


STEP_CODE_MAP = {
    NORTH: "^",
    SOUTH: "v",
    EAST: ">",
    WEST: "<",
}

@cache
def plan_remote_code(code: str, sub_levels=0):
    return plan_code(code, get_remote_control(), sub_levels=sub_levels)


def plan_code(code: str, grid: Grid, sub_levels=0):
    plan = ""
    best_sub_plan_length = 0
    start_location = grid.find_one("A")
    location = start_location
    for char in code:
        char_steps = []
        target_location = grid.find_one(char)
        while target_location - location != get_vector(0, 0):
            for step in grid.traverse_order:
                if is_manhattan_component(step, target_location - location):
                    location = location + step
                    char_steps.append(step)
                    break

        if sub_levels == 0:
            char_plan = "".join(STEP_CODE_MAP[step] for step in char_steps) + "A"
            best_char_sub_plan_length = len(char_plan)

        else:
            char_plan = ""
            best_char_sub_plan_length = inf
            for candidate_char_plan in permutations(char_steps, len(char_steps)):
                valid = True
                candidate_location = start_location
                for step in candidate_char_plan:
                    candidate_location += step
                    if grid[candidate_location] == " ":
                        valid = False
                        break
                if not valid:
                    continue
                candidate_char_plan = (
                    "".join(STEP_CODE_MAP[step] for step in candidate_char_plan) + "A"
                )
                _, char_sub_plan_length = plan_remote_code(
                    candidate_char_plan,
                    sub_levels=sub_levels - 1,
                )
                if char_sub_plan_length < best_char_sub_plan_length:
                    best_char_sub_plan_length = char_sub_plan_length
                    char_plan = candidate_char_plan

            assert char_plan != ""

        plan += char_plan
        best_sub_plan_length += best_char_sub_plan_length
        start_location = target_location

    return plan, best_sub_plan_length


def solve_code(code, remotes = 3) -> int:
    keypad = get_keypad()
    #remote = get_remote_control()

    #print(f"Code: {code}")
    remote_code, total_code_length = plan_code(code, keypad, sub_levels=remotes - 1)
    # print(f"Remote 0: {remote_code}")
    # for i in range(1, remotes):
    #     remote_code, _ = plan_code(remote_code, remote, sub_levels=remotes - i - 1)
    #     print(f"Remote {i}: {remote_code}")
    return total_code_length


def solve_part_1(puzzle_input):
    complexity_sum = 0
    for code in puzzle_input:
        total_code_length = solve_code(code, remotes=3)
        print(f"{code}: len(plan) * int(code[:-1]): {total_code_length} * {int(code[:-1])}")

    return complexity_sum


def solve_part_2(puzzle_input):
    complexity_sum = 0
    for code in puzzle_input:
        total_code_length = solve_code(code, remotes=26)
        print(f"{code}: len(plan) * int(code[:-1]): {total_code_length} * {int(code[:-1])}")
        complexity_sum += total_code_length * int(code[:-1])
    return complexity_sum


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--example", action="store_true")
    args = parser.parse_args()

    puzzle_input = get_puzzle_input(use_example=args.example)

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")
