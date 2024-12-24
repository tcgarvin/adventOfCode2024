import argparse
from functools import cache
from rich import print
from rich.progress import track

def get_puzzle_input(use_example=False):
    input_filename = "example.txt" if use_example else "input.txt"
    towels = []
    patterns = []
    with open(input_filename) as input_txt:
        lines = input_txt.readlines()
        towels = tuple(lines[0].strip().split(", "))
        patterns = tuple(line.strip() for line in lines[2:])
    return towels, patterns

def is_compatable(towel, pattern):
    return pattern.startswith(towel)

def solve_pattern(pattern, towels) -> list[str]:
    answer = []
    for towel in towels:
        if towel == pattern:
            return [towel]

        if is_compatable(towel, pattern):
            sub_towels = solve_pattern(pattern[len(towel):], towels)
            if len(sub_towels) > 0:
                answer = [towel] + sub_towels
                break

    if len(answer) > 0:
        assert "".join(answer) == pattern
        
    return answer

def solve_part_1(towels, patterns):
    solvable_patterns = 0
    for pattern in track(patterns):
        answer = solve_pattern(pattern, towels)
        if len(answer) > 0:
            solvable_patterns += 1

    return solvable_patterns

def _get_solver(towels):

    @cache
    def solver(pattern) -> int:
        if len(pattern) == 0:
            return 1

        answer = 0
        for towel in towels:
            if is_compatable(towel, pattern):
                answer += solver(pattern[len(towel):])

        return answer

    return solver

def solve_part_2(towels, patterns):
    design_count = 0
    for pattern in track(patterns):
        solver = _get_solver(towels)
        answer = solver(pattern)
        design_count += answer
    return design_count

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--example", action="store_true")
    args = parser.parse_args()

    towels, patterns = get_puzzle_input(use_example=args.example)

    answer_1 = solve_part_1(towels, patterns)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(towels, patterns)
    print(f"Part 2: {answer_2}")
