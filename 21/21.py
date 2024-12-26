import argparse
from itertools import permutations
from rich import print

from grid import Grid, Vector, get_vector, NORTH, SOUTH, EAST, WEST, grid_from_input_txt, print_grid

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

def is_manhattan_component(component:Vector, whole:Vector):
    # Assumes component is a unit vector north south east or west
    return (component.j > 0 and whole.j > 0 or
            component.j < 0 and whole.j < 0 or 
            component.i > 0 and whole.i > 0 or
            component.i < 0 and whole.i < 0)

STEP_CODE_MAP = {
    NORTH: "^",
    SOUTH: "v",
    EAST: ">",
    WEST: "<",
}

def plan_code(code:str, grid:Grid, sub_levels=0):
    candidate_remote_control = get_remote_control()
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
            best_char_sub_plan_length = 500
            for candidate_char_plan in permutations(char_steps, len(char_steps)):
                valid = True
                location = start_location
                for step in candidate_char_plan:
                    location += step
                    if grid[location] == " ":
                        valid = False
                        break
                if not valid:
                    continue
                candidate_char_plan = "".join(STEP_CODE_MAP[step] for step in candidate_char_plan) + "A"
                _, char_sub_plan_length = plan_code(candidate_char_plan, candidate_remote_control, sub_levels=sub_levels-1)
                if char_sub_plan_length < best_char_sub_plan_length:
                    best_char_sub_plan_length = char_sub_plan_length
                    char_plan = candidate_char_plan

        plan += char_plan
        best_sub_plan_length += best_char_sub_plan_length

    return plan, best_sub_plan_length


def solve_code_1(code):
    keypad = get_keypad()
    remote = get_remote_control()

    print(f"Code: {code}")
    remote1_code, _ = plan_code(code, keypad, sub_levels=2)
    print(f"Remote 1: {remote1_code}")
    remote2_code, _ = plan_code(remote1_code, remote, sub_levels=1)
    print(f"Remote 2: {remote2_code}")
    remote3_code, _ = plan_code(remote2_code, remote, sub_levels=0)
    print(f"Remote 3: {remote3_code}")
    return remote3_code


def solve_part_1(puzzle_input):
    complexity_sum = 0
    for code in puzzle_input:
        plan = solve_code_1(code)
        print(f"{code}: len(plan) * int(code[:-1]): {len(plan)} * {int(code[:-1])}")
        complexity_sum += len(plan) * int(code[:-1])
        
    return complexity_sum

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
