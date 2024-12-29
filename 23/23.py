import argparse
from collections import Counter
from itertools import combinations
from functools import cache, partial
from rich import print
from rich.progress import track

def get_puzzle_input(use_example=False):
    input_filename = "example.txt" if use_example else "input.txt"
    puzzle_input = []
    with open(input_filename) as input_txt:
        for line in input_txt:
            puzzle_input.append(set(x.strip() for x in line.split("-")))
    return puzzle_input

def solve_part_1(computer_links):
    computers = set()
    for link in computer_links:
        computers.update(link)

    # Using a set instead of a list saves about 90%
    sorted_links = set(tuple(sorted(link)) for link in computer_links)
    networked_groups_of_three = []
    for group_of_three in track(list(combinations(computers, 3))):

        # Filter for "t" here saves about 75%
        if all(not c.startswith("t") for c in group_of_three):
            continue

        needed_links = list(tuple(sorted(c)) for c in combinations(group_of_three, 2))
        if all(link in sorted_links for link in needed_links):
            networked_groups_of_three.append(group_of_three)

    groups_with_t_count = 0
    for group_of_three in networked_groups_of_three:
        if any(computer.startswith("t") for computer in group_of_three):
            groups_with_t_count += 1
        
    return groups_with_t_count

def is_completely_connected(group: set[str], bidirectional_links: set[tuple[str, str]]) -> bool:
    for c1, c2 in combinations(group, 2):
        if (c1, c2) not in bidirectional_links:
            return False
    return True

def solve_part_2(computer_links):
    # Not sure we need to have these sorted right now, but I like it better than
    # the initial parsing.
    sorted_links = set(tuple(sorted(link)) for link in computer_links)
    reversed_links = set(tuple(reversed(sorted(link))) for link in computer_links)
    bidirectional_links = sorted_links | reversed_links
    computer_count = Counter()
    for link in sorted_links:
        computer_count[link[0]] += 1
        computer_count[link[1]] += 1

    #print(computer_count)

    # Prior analysis shows all computers have 13 neighbors, which gives us an upper bound on cluster size
    for i in range(3,15):
        cached_is_completely_connected = cache(partial(is_completely_connected, bidirectional_links=bidirectional_links))
        clusters_found = set()
        for computer in track(list(computer_count.keys()), f"Cluster size {i}"):
            neighbors = set([computer])
            for key in bidirectional_links:
                if key[0] == computer:
                    neighbors.add(key[1])

            for group in combinations(neighbors, i):
                if cached_is_completely_connected(group):
                    clusters_found.add(tuple(sorted(group)))
        print(f"Found {len(clusters_found)} clusters of size {i}")
        if len(clusters_found) == 1:
            return ",".join(sorted(clusters_found.pop()))
    
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--example", action="store_true")
    args = parser.parse_args()

    puzzle_input = get_puzzle_input(use_example=args.example)

    #answer_1 = solve_part_1(puzzle_input)
    #print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")
