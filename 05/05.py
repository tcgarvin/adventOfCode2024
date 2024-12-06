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

        correct_order = True
        for ordering_rule in ordering_rules:
            if (
                update_page_set.issuperset(ordering_rule) 
                and update.index(ordering_rule[0]) > update.index(ordering_rule[1])
            ):
                correct_order = False
                break

        if correct_order:
            continue

        order_rule_numbers = set()
        relevant_ordering_rules = []
        for ordering_rule in ordering_rules:
            if update_page_set.issuperset(ordering_rule):
                order_rule_numbers.update(ordering_rule)
                relevant_ordering_rules.append(ordering_rule)

        assert order_rule_numbers == update_page_set

        # If we assume that the ordering rules must cover enough information to
        # get halfway through the update, we should be OK.

        # Thought. The lowest number should not by on the right side of any relevant rule.
        ordered_update = []
        unordered_pages = set(update_page_set)
        while len(ordered_update) < (len(update) // 2) + 1:
            numbers_above = set(x[1] for x in relevant_ordering_rules)
            numbers_below = unordered_pages - numbers_above
            if len(numbers_below) != 1:
                print("Update:", update)
                print("Rules:", relevant_ordering_rules)
                print(numbers_above)
                raise Exception("Expected one number below, but got: ", numbers_below)

            next_number = numbers_below.pop()
            ordered_update.append(next_number)

            relevant_ordering_rules = [o for o in relevant_ordering_rules if next_number not in o]
        
        total += ordered_update[len(ordered_update) // 2]

    return total


if __name__ == "__main__":
    ordering_rules, updates = get_puzzle_input()

    answer_1 = solve_part_1(ordering_rules, updates)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(ordering_rules, updates)
    print(f"Part 2: {answer_2}")
