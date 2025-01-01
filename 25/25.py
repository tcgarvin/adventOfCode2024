import argparse
from collections import Counter
from rich import print

def get_puzzle_input(use_example=False):
    input_filename = "example.txt" if use_example else "input.txt"
    locks = []
    keys = []
    current_item = None
    pin_heights = Counter()
    with open(input_filename) as input_txt:
        for line in input_txt:
            line = line.strip()
            if current_item is None and line == "#####":
                current_item = "lock"
                pin_heights = Counter()
                locks.append(pin_heights)

            elif current_item is None and len(line) > 0:
                current_item = "key"
                pin_heights = Counter()
                keys.append(pin_heights)

            for i, char in enumerate(line):
                if char == "#":
                    pin_heights[i] += 1

            if line == "":
                current_item = None

    return locks, keys

def fits(lock, key):
    return not any(lock[i] + key[i] > 7 for i in range(5))

def solve_part_1(locks, keys):
    compatible_combinations = 0
    for lock in locks:
        for key in keys:
            if fits(lock, key):
                compatible_combinations += 1
    return compatible_combinations

def solve_part_2(locks, keys):
    return ""

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--example", action="store_true")
    args = parser.parse_args()

    locks, keys = get_puzzle_input(use_example=args.example)

    answer_1 = solve_part_1(locks, keys)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(locks, keys)
    print(f"Part 2: {answer_2}")
