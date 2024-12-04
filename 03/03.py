import re

from rich import print

MUL_RE = re.compile("""
    do[(][)]
    |
    don[']t[(][)]
    |
    mul
    [(]
    ([0-9]{1,3})
    ,
    ([0-9]{1,3})
    [)]
""",re.X)

def get_puzzle_input():
    puzzle_input = ""
    with open("input.txt") as input_txt:
        puzzle_input = input_txt.read()
    return puzzle_input

def solve_part_1(puzzle_input):
    matches = MUL_RE.finditer(puzzle_input)
    total = 0
    for m in matches:
        if m.group(0).startswith("do"):
            continue
        total += int(m.group(1)) * int(m.group(2))
    return total

def solve_part_2(puzzle_input):
    matches = MUL_RE.finditer(puzzle_input)
    total = 0
    enabled = True
    for m in matches:
        if m.group(0) == "do()":
            enabled = True
        elif m.group(0) == "don't()":
            enabled = False
        elif enabled:
            total += int(m.group(1)) * int(m.group(2))
    return total

if __name__ == "__main__":
    puzzle_input = get_puzzle_input()

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")
