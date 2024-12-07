from itertools import cycle
from time import time

from rich import print
from rich.progress import Progress, TextColumn, BarColumn, TaskProgressColumn, TimeElapsedColumn, MofNCompleteColumn

from grid import Grid, Vector, grid_from_input_txt, NORTH, EAST, SOUTH, WEST


def get_puzzle_input():
    input_filename = "input.txt"
    #input_filename = "example.txt"
    with open(input_filename) as input_txt:
        return grid_from_input_txt(input_txt.read(), "O")

def traverse(grid:Grid, mark=None):
    location_direction_seen = set()
    def guard_status(location:Vector, direction:Vector):
        if grid[location] == "O":
            return "off-grid"
        location_direction = (location, direction)
        if location_direction in location_direction_seen:
            return "loop"
        location_direction_seen.add(location_direction)
        return "live"

    location = grid.find_one("^")
    rotation = cycle([NORTH, EAST, SOUTH, WEST])  # Note, Starting with NORTH
    direction = next(rotation)
    status = "live"
    while status == "live":
        if mark is not None:
            grid[location] = mark
        while grid[location + direction] == "#":
            direction = next(rotation)
            status = guard_status(location, direction)

        location += direction
        status = guard_status(location, direction)

    return status

def solve_part_1(grid: Grid):
    traverse(grid, mark="X")

    print(len(grid.grid))
    return len(list(grid.find("X"))), list(grid.find("X"))

def solve_part_2(grid:Grid, candidate_locations):
    loop_count = 0
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TimeElapsedColumn(),
        MofNCompleteColumn(),
        TextColumn("Loop Count: {task.fields[loop_count]}"),
    ) as progress:
        task = progress.add_task("Searching", total=len(candidate_locations), loop_count=loop_count)
        for modification_location in candidate_locations:
            if grid[modification_location] == "^":
                continue
            grid[modification_location] = "#"
            status = traverse(grid)
            if status == "loop":
                loop_count += 1
            grid[modification_location] = "."
            progress.update(task, advance=1, loop_count=loop_count)

    return loop_count

if __name__ == "__main__":
    answer_1, x_locations = solve_part_1(get_puzzle_input())
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(get_puzzle_input(), x_locations)
    print(f"Part 2: {answer_2}")
