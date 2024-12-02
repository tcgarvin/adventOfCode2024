from rich import print

def get_puzzle_input():
    puzzle_input = []
    with open("input.txt") as input_txt:
        for line in input_txt:
            numbers_strings = line.strip().split()
            numbers = [int(num) for num in numbers_strings]
            puzzle_input.append(numbers)
    return puzzle_input

def is_safe(row: list[int]) -> bool:
    pairs = [row[i:i+2] for i in range(len(row) - 1)]
    if any(abs(a - b) > 3 for a, b in pairs):
        return False
    if any(a == b for a, b in pairs):
        return False
    if any(a < b for a, b in pairs) and any(a > b for a, b in pairs):
        return False

    return True

def is_safe_2(row: list[int]) -> bool:
    print("Row:", row)
    if is_safe(row):
        return True

    for i in range(len(row)):
        print("Subrow:", row[:i] + row[i + 1:])
        if is_safe(row[:i] + row[i + 1:]):
            print("(Safe)")
            return True

    return False
    

def solve_part_1(puzzle_input):
    return sum(is_safe(row) for row in puzzle_input)

def solve_part_2(puzzle_input):
    return sum(is_safe_2(row) for row in puzzle_input)

if __name__ == "__main__":
    puzzle_input = get_puzzle_input()

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")
