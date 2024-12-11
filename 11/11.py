import argparse
from functools import cache
from rich import print

def get_puzzle_input(use_example=False):
    input_filename = "example.txt" if use_example else "input.txt"
    puzzle_input = []
    with open(input_filename) as input_txt:
        puzzle_input = [int(x) for x in input_txt.read().split()]
    return puzzle_input

@cache
def blink(stone:int, blinks:int) -> int:
    if blinks == 0:
        return 1

    new_stones = None
    if stone == 0:
        new_stones = (1,)
    elif stone >= 10 and len(stone_digits := str(stone)) % 2 == 0:
        midpoint = len(stone_digits)//2
        new_stones = (int(stone_digits[:midpoint]), int(stone_digits[midpoint:]))
    else:
        new_stones = ((stone * 2024),)

    blinks -= 1
    return sum(blink(stone, blinks) for stone in new_stones)

def solve_part_1(puzzle_input):
    return sum(blink(stone, 25) for stone in puzzle_input)

def solve_part_2(puzzle_input):
    return sum(blink(stone, 75) for stone in puzzle_input)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--example", action="store_true")
    args = parser.parse_args()

    puzzle_input = get_puzzle_input(use_example=args.example)

    answer_1 = solve_part_1(puzzle_input)
    #print(f"Cache size: {blink.cache_info().currsize}")
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    #print(f"Cache size: {blink.cache_info().currsize}")
    print(f"Part 2: {answer_2}")
