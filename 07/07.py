import argparse
from rich import print

def get_puzzle_input(use_example=False):
    input_filename = "example.txt" if use_example else "input.txt"
    puzzle_input = []
    with open(input_filename) as input_txt:
        for line in input_txt:
            numbers = [int(token) for token in line.replace(":", "").split()]
            test_value = numbers[0]
            component_numbers = numbers[1:]

            puzzle_input.append((test_value, component_numbers))
    return puzzle_input

def mul(args):
    """Like sum, but multiplies."""
    result = 1
    for arg in args:
        result *= arg
    return result

def is_possible(numbers, target, use_concat=False):
    if len(numbers) == 1 and numbers[0] == target:
        return True

    elif len(numbers) == 1:
        return False

    elif numbers[0] > target:
        return False

    # Try multiplcation
    multiplied = [numbers[0] * numbers[1]] + numbers[2:]
    if is_possible(multiplied, target, use_concat):
        return True

    # Try addition
    summed = [numbers[0] + numbers[1]] + numbers[2:]
    if is_possible(summed, target, use_concat):
        return True

    # Try concatenation
    if use_concat:
        concatenated = [int(str(numbers[0]) + str(numbers[1]))] + numbers[2:]
        if is_possible(concatenated, target, use_concat):
            return True
    
    return False

def solve_part_1(puzzle_input):
    total = 0
    for test_value, component_numbers in puzzle_input:
        #if sum(component_numbers) > test_value or mul(component_numbers) < test_value:
            #continue

        if is_possible(component_numbers, test_value):
            total += test_value
    return total 

def solve_part_2(puzzle_input):
    total = 0
    for test_value, component_numbers in puzzle_input:
        if is_possible(component_numbers, test_value, use_concat=True):
            total += test_value
    return total

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--example", action="store_true")
    args = parser.parse_args()

    puzzle_input = get_puzzle_input(use_example=args.example)

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")
