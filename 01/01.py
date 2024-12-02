from rich import print
from collections import Counter

def get_puzzle_input():
    puzzle_input = []
    with open("input.txt") as input_txt:
        for line in input_txt:
            numbers_strings = line.strip().split()
            numbers = [int(num) for num in numbers_strings]
            puzzle_input.append(numbers)
    return puzzle_input

def solve_part_1(puzzle_input):
    list1, list2 = list(zip(*puzzle_input))
    sorted_list1 = sorted(list1)
    sorted_list2 = sorted(list2)

    total = 0
    for row_number in range(len(puzzle_input)):
        number1 = sorted_list1[row_number]
        number2 = sorted_list2[row_number]
        distance = abs(number1 - number2)
        total = total + distance

    return total

def solve_part_2(puzzle_input):
    list1, list2 = list(zip(*puzzle_input))
    counter = Counter(list2)
    # print(counter)

    total = 0
    for row_number in range(len(puzzle_input)):
        number1 = list1[row_number]
        number_count = counter.get(number1, 0)
        total = total + (number1 * number_count)

    return total

if __name__ == "__main__":
    puzzle_input = get_puzzle_input()
    print(puzzle_input)

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")
