import argparse
from rich import print

def get_puzzle_input(use_example=False):
    input_filename = "input.txt"
    if use_example:
        input_filename = "example.txt"
    puzzle_input = []
    with open(input_filename) as input_txt:
        for line in input_txt:
            puzzle_input.append(line)
    return puzzle_input

def solve_part_1(puzzle_input):
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
