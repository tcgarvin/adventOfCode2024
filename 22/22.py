import argparse
from rich import print
from rich.progress import track
from collections import Counter

def get_puzzle_input(use_example=False):
    input_filename = "example.txt" if use_example else "input.txt"
    puzzle_input = []
    with open(input_filename) as input_txt:
        puzzle_input = [int(l) for l in input_txt]
    return puzzle_input

def evolve(secret: int) -> int:
    secret = ((secret * 64) ^ secret) % 16777216
    secret = ((secret // 32) ^ secret) % 16777216
    secret = ((secret * 2048) ^ secret)  % 16777216
    return secret

def evolve_times(secret: int, times: int) -> int:
    for _ in range(times):
        secret = evolve(secret)
    return secret

def solve_part_1(puzzle_input):
    total = 0
    for start_secret in puzzle_input:
        total += evolve_times(start_secret, 2000)
    return total

def get_buyer_sequence_map(start_secret: int) -> dict[tuple[int, int, int, int], int]:
    buyer_sequence_map = {}
    change_sequence = []
    secret = start_secret
    for _ in range(2000):
        next_secret = evolve(secret)
        change_sequence.append((next_secret % 10) - (secret % 10))
        secret = next_secret
        price = secret % 10
        if len(change_sequence) >= 4:
            last_four_changes = tuple(change_sequence[-4:])
            if last_four_changes not in buyer_sequence_map:
                buyer_sequence_map[last_four_changes] = price
    return buyer_sequence_map

def solve_part_2(puzzle_input):
    totals = Counter()
    for start_secret in track(puzzle_input):
        totals.update(get_buyer_sequence_map(start_secret))
    return totals.most_common(1)[0][1]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--example", action="store_true")
    args = parser.parse_args()

    puzzle_input = get_puzzle_input(use_example=args.example)

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")
