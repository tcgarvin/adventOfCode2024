from rich import print

def get_puzzle_input():
    ordering_rules = []
    updates = []
    
    with open("input.txt") as input_txt:
        for line in input_txt:
            if "|" in line:
                ordering_rule = [int(num) for num in line.strip().split("|")]
                ordering_rules.append(ordering_rule)
            elif "," in line:
                update = [int(num) for num in line.strip().split(",")]
                updates.append(update)

    return ordering_rules, updates

def solve_part_1(ordering_rules: list[list[int]], updates: list[list[int]]):
    total = 0
    for update in updates:
        update_page_set = set(update)
        correct_order = True
        for ordering_rule in ordering_rules:
            if (
                update_page_set.issuperset(ordering_rule) 
                and update.index(ordering_rule[0]) > update.index(ordering_rule[1])
            ):
                correct_order = False
                break

        if correct_order:
            total += update[len(update) // 2]
        
    return total

def solve_part_2(ordering_rules: list[list[int]], updates: list[list[int]]):
    total = 0
    for update in updates:
        update_page_set = set(update)

        correct_original_order = True
        correct_current_order = None
        while correct_current_order is not True:
            correct_current_order = True
            for ordering_rule in ordering_rules:
                if (
                    update_page_set.issuperset(ordering_rule) 
                    and update.index(ordering_rule[0]) > update.index(ordering_rule[1])
                ):
                    correct_original_order = False
                    correct_current_order = False
                    a = update.index(ordering_rule[0])
                    b = update.index(ordering_rule[1])
                    update[a], update[b] = update[b], update[a]
                    break

        if not correct_original_order:
            total += update[len(update) // 2]

    return total


if __name__ == "__main__":
    ordering_rules, updates = get_puzzle_input()

    answer_1 = solve_part_1(ordering_rules, updates)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(ordering_rules, updates)
    print(f"Part 2: {answer_2}")
