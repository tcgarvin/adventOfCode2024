import argparse
from rich import print

def get_puzzle_input(use_example=False):
    input_filename = "example.txt" if use_example else "input.txt"
    puzzle_input = ""
    with open(input_filename) as input_txt:
        puzzle_input = [int(c) for c in input_txt.read().strip()]
    return puzzle_input

def disk_layout(puzzle_input):
    disk = []
    for i in range(0, len(puzzle_input), 2):
        file_id = i // 2
        disk.extend([file_id] * puzzle_input[i])
        if i + 1 < len(puzzle_input):
            disk.extend([None] * puzzle_input[i+1])

    return disk

def checksum(disk):
    checksum = 0
    for i, file_id in enumerate(disk):
        if file_id is not None:
            checksum += i * file_id
        
    return checksum

def solve_part_1(puzzle_input):
    disk = disk_layout(puzzle_input)

    #print(len(disk))
    #print(disk[:20])

    cursor1 = 0
    cursor2 = len(disk) - 1
    while True:
        while disk[cursor1] is not None:
            cursor1 += 1

        while disk[cursor2] is None:
            cursor2 -= 1

        if cursor1 >= cursor2:
            break

        disk[cursor1] = disk[cursor2]
        disk[cursor2] = None

    return checksum(disk)

ALNUM = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
def print_disk(disk):
    print("".join([ALNUM[f % len(ALNUM)] if f is not None else "." for f in disk]))

def solve_part_2(puzzle_input):
    disk = disk_layout(puzzle_input)

    #print_disk(disk)

    cursor2 = len(disk) - 1
    while cursor2 > 0:
        while disk[cursor2] is None:
            cursor2 -= 1

        file_id = disk[cursor2]
        if cursor2 < len(disk) - 1:
            assert disk[cursor2 + 1] != file_id
        #print(file_id)
        file_end_index = cursor2 + 1
        file_start_index = None
        while disk[cursor2] is file_id:
            file_start_index = cursor2
            cursor2 -= 1

        file_length = file_end_index - file_start_index
        required_empty_block = [None] * file_length
        #print(required_empty_block)

        cursor1 = 0
        found_empty_block = False
        while cursor1 <= cursor2:
            if disk[cursor1:cursor1+file_length] == required_empty_block:
                found_empty_block = True
                break
            cursor1 += 1

        if found_empty_block:
            assert cursor1 < file_start_index
            #print(f"Found empty block at {cursor1}: {disk[cursor1:cursor1+file_length]}")
            print(f"Moving file {file_id} (len {file_length}) from {file_start_index} to {cursor1}")
            #print(f"{disk[file_start_index:file_end_index]}")
            disk[cursor1:cursor1+file_length] = [file_id] * file_length
            disk[file_start_index:file_end_index] = required_empty_block
            #print_disk(disk)

    #print_disk(disk)
    return checksum(disk)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--example", action="store_true")
    parser.add_argument("--random", action="store_true")
    args = parser.parse_args()

    if not args.random:
        puzzle_input = get_puzzle_input(use_example=args.example)
    else:
        import random
        #puzzle_input = random.choices(range(1,10), k = 11)
        puzzle_input = [1,1,1,1,1,1,1,1,1,1,1]

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")
