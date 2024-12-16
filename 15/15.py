import argparse
from rich import print
from rich.progress import track

from grid import grid_from_input_txt, Grid, NORTH, EAST, SOUTH, WEST, Vector, print_grid

movemap = {
    "^": NORTH,
    ">": EAST,
    "v": SOUTH,
    "<": WEST,
}

def get_puzzle_input(use_example=False):
    input_filename = "example.txt" if use_example else "input.txt"
    grid = None
    with open(input_filename) as input_txt:
        gridlines = ""
        movelines = ""
        for line in input_txt:
            if "#" in line:
                gridlines += line

            else:
                movelines += line.strip()

    grid = grid_from_input_txt(gridlines)
    moves = [movemap[m] for m in movelines]
    print_grid(grid)
    return grid, moves

def get_puzzle_input_2(use_example=False):
    input_filename = "example.txt" if use_example else "input.txt"
    grid = None
    with open(input_filename) as input_txt:
        gridlines = ""
        movelines = ""
        for line in input_txt:
            if "#" in line:
                for c in line:
                    if c == "@":
                        gridlines += "@."
                    elif c == "O":
                        gridlines += "[]"
                    elif c == "\n":
                        gridlines += "\n"
                    else:
                        gridlines += c + c
            else:
                movelines += line.strip()

    grid = grid_from_input_txt(gridlines)
    moves = [movemap[m] for m in movelines]
    print_grid(grid)
    return grid, moves

def push(grid:Grid, source:Vector, direction:Vector) -> bool:
    target = source + direction
    success = False
    if grid[target] == "#":
        success = False

    elif grid[target] == ".":
        success = True

    elif grid[target] == "O":
        success = push(grid, target, direction)

    else:
        raise Exception("What is this")

    if success:
        grid[target] = grid[source]
        grid[source] = "."
    
    return success


def solve_part_1(grid:Grid, moves:list[Vector]):
    for move in track(moves):
        push(grid, grid.find_one('@'), move)

    print_grid(grid)

    total_gps = 0
    for box_location in grid.find("O"):
        gps = 100 * box_location.i + box_location.j
        total_gps += gps


    return total_gps

def push_2(grid:Grid, source:Vector, direction:Vector, commit=False) -> bool:
    target = source + direction
    success = False
    if grid[target] == "#":
        success = False

    elif grid[target] == ".":
        success = True

    elif grid[target] == "[":
        success = push_box_2(grid, target, direction, commit=commit)

    elif grid[target] == "]":
        success = push_box_2(grid, target + WEST, direction, commit=commit)

    else:
        raise Exception(f"What is this: {grid[target]}")

    if success and commit:
        grid[target] = grid[source]
        grid[source] = "."
    
    return success


def push_box_2(grid:Grid, source:Vector, direction:Vector, commit=False) -> bool:
    if grid[source] != "[":
        raise Exception("Bad source")

    potential_blocks = tuple()
    if direction == EAST:
        potential_blocks = ((source + (EAST * 2)),)
    elif direction == WEST:
        potential_blocks = ((source + WEST),)
    elif direction == NORTH:
        potential_blocks = (source + NORTH, source + EAST + NORTH)
    elif direction == SOUTH:
        potential_blocks = (source + SOUTH, source + EAST + SOUTH)

    checked_blocks = set()
    success = True
    for potential_block in potential_blocks:
        if grid[potential_block] == ".":
            continue
        elif grid[potential_block] == "#":
            success = False
        elif grid[potential_block] == "[" and potential_block not in checked_blocks:
            success = success and push_box_2(grid, potential_block, direction, commit=commit)
        elif grid[potential_block] == "]":
            potential_block += WEST
            if potential_block not in checked_blocks:
                success = success and push_box_2(grid, potential_block, direction, commit=commit)

        checked_blocks.add(potential_block)

    if success and commit:
        grid[source] = "."
        grid[source + EAST] = "."
        grid[source + direction] = "["
        grid[source + EAST + direction] = "]"
    
    return success



def solve_part_2(grid, moves):
    for i,move in track(list(enumerate(moves))):
        source = grid.find_one('@')
        can_commit = push_2(grid, source, move, commit=False)
        if can_commit:
            push_2(grid, source, move, commit=True)

        #print_grid(grid)
        #print(f"^^^ After {i}")

    print_grid(grid)

    total_gps = 0
    for box_location in grid.find("["):
        gps = 100 * box_location.i + box_location.j
        total_gps += gps

    return total_gps

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--example", action="store_true")
    args = parser.parse_args()

    grid, moves = get_puzzle_input(use_example=args.example)
    answer_1 = solve_part_1(grid, moves)
    print(f"Part 1: {answer_1}")

    grid2, moves2 = get_puzzle_input_2(use_example=args.example)
    answer_2 = solve_part_2(grid2, moves2)
    print(f"Part 2: {answer_2}")
