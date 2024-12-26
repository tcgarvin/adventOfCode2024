import argparse
from rich import print
from rich.progress import track
from itertools import count

from grid import grid_from_input_txt, Grid, Vector, get_vector, CARDINAL_DIRECTIONS

def get_puzzle_input(use_example=False) -> Grid:
    input_filename = "example.txt" if use_example else "input.txt"
    puzzle_input = None
    with open(input_filename) as input_txt:
        puzzle_input = grid_from_input_txt(input_txt.read(), out_of_bounds="#")
    return puzzle_input

def solve_part_1(grid:Grid):
    distance_map = {}
    start_location = grid.find_one("S")
    location = start_location
    distance = 0
    logged_end = False
    while not logged_end:
        distance_map[location] = distance
        distance += 1
        if grid[location] == "E":
            logged_end = True
        else:
            for direction in CARDINAL_DIRECTIONS:
                next_location = location + direction
                if grid[next_location] != "#" and next_location not in distance_map:
                    break

            location = next_location

    print(distance)

    cheats = {}
    for path_location in distance_map.keys():
        for direction in CARDINAL_DIRECTIONS:
            neighbor = path_location + direction
            cheat_location = path_location + direction * 2
            if grid[neighbor] == "#" and grid[cheat_location] in ".E":
                cheat_value = distance_map[cheat_location] - distance_map[path_location] - 2
                if cheat_value > 0:
                    cheats[(path_location, direction)] = cheat_value

    return len([v for v in cheats.values() if v >= 100])

def solve_part_2(grid:Grid) -> int:
    distance_map = {}
    start_location = grid.find_one("S")
    location = start_location
    distance = 0
    logged_end = False
    while not logged_end:
        distance_map[location] = distance
        distance += 1
        if grid[location] == "E":
            logged_end = True
        else:
            for direction in CARDINAL_DIRECTIONS:
                next_location = location + direction
                if grid[next_location] != "#" and next_location not in distance_map:
                    break

            location = next_location

    print(distance)

    cheat_vectors = []
    for i in range(-20, 21):
        compliment = 20 - abs(i)
        for j in range(-compliment, compliment+1):
            if abs(i) > 1 or abs(j) > 1:
                cheat_vectors.append(get_vector(i, j))

    cheats = {}
    for path_location in track(list(distance_map.keys())):
        for cheat_vector in cheat_vectors:
            cheat_location = path_location + cheat_vector
            if grid[cheat_location] in ".E":
                cheat_length = abs(cheat_vector.i) + abs(cheat_vector.j)
                cheat_value = distance_map[cheat_location] - distance_map[path_location] - cheat_length
                if cheat_value >= 100:
                    cheats[(path_location, cheat_location)] = cheat_value

    return len(cheats)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--example", action="store_true")
    args = parser.parse_args()

    puzzle_input = get_puzzle_input(use_example=args.example)

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")
