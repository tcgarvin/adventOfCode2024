import argparse
from typing import Set
from rich import print

from grid import Grid, Vector, grid_from_input_txt, NORTH, EAST, SOUTH, WEST


def get_puzzle_input(use_example=False):
    input_filename = "example.txt" if use_example else "input.txt"
    puzzle_input = None
    with open(input_filename) as input_txt:
        puzzle_input = grid_from_input_txt(input_txt.read(), out_of_bounds=".")
    return puzzle_input


def score_region(
    grid: Grid, region_grid: Grid, location: Vector
) -> tuple[int, int, Set[Vector]]:
    """Returns a tuple of (area, perimeter)"""
    # Region grid is like a "seen" set.
    if region_grid[location] != ".":
        return (0, 0, set())

    region_grid[location] = "X"

    area = 1
    perimeter = 0
    membership = set([location])
    for direction in [NORTH, EAST, SOUTH, WEST]:
        new_location = location + direction
        if grid[new_location] == grid[location]:
            downstream_area, downstream_perimeter, downstream_membership = score_region(
                grid, region_grid, new_location
            )
            area += downstream_area
            perimeter += downstream_perimeter
            membership.update(downstream_membership)
        else:
            perimeter += 1

    return (area, perimeter, membership)


def solve_part_1(grid: Grid):
    region_grid = Grid(out_of_bounds=".")
    score = 0
    for location in grid.all_locations():
        if region_grid[location] != ".":
            continue

        area, permimeter, _ = score_region(grid, region_grid, location)
        score += area * permimeter

    return score


def count_sides(region_locations: Set[Vector]) -> int:
    segments = set()
    for location in region_locations:
        for direction in [NORTH, EAST, SOUTH, WEST]:
            neighbor = location + direction
            if neighbor not in region_locations:
                segments.add((location, direction))

    # group segments
    side_count = 0
    counted_segments = set()
    for segment in segments:
        if segment in counted_segments:
            continue
        counted_segments.add(segment)

        side_direction = segment[1]
        if side_direction in (NORTH, SOUTH):
            # Look west and east
            for seek_direction in (EAST, WEST):
                side_cursor = segment[0] + seek_direction
                while (side_cursor, side_direction) in segments:
                    counted_segments.add((side_cursor, side_direction))
                    side_cursor += seek_direction

        elif side_direction in (EAST, WEST):
            # Look north and south
            for seek_direction in (NORTH, SOUTH):
                side_cursor = segment[0] + seek_direction
                while (side_cursor, side_direction) in segments:
                    counted_segments.add((side_cursor, side_direction))
                    side_cursor += seek_direction

        side_count += 1
    return side_count


def solve_part_2(grid: Grid):
    region_grid = Grid(out_of_bounds=".")
    score = 0
    for location in grid.all_locations():
        if region_grid[location] != ".":
            continue

        area, _, region_locations = score_region(grid, region_grid, location)
        score += area * count_sides(region_locations)

    return score


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--example", action="store_true")
    args = parser.parse_args()

    puzzle_input = get_puzzle_input(use_example=args.example)

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")
