import argparse
from itertools import combinations
from math import comb
from rich import print
from typing import NamedTuple

Gate = NamedTuple("Gate", [("input1", str), ("gate", str), ("input2", str), ("output", str)])   

def get_puzzle_input(use_example=False):
    input_filename = "example.txt" if use_example else "input.txt"
    values = {}
    gates = []
    with open(input_filename) as input_txt:
        for line in input_txt:
            if ":" in line:
                gate, value = line.strip().split(": ")
                values[gate] = int(value)

            elif "->" in line:
                input1, gate, input2, _, output = line.strip().split()
                gates.append(Gate(input1, gate, input2, output))
    return values, gates

def run_logic_xy(x:int, y:int, bits:int, gates:list[Gate]) -> int:
    values = {}
    for i in range(bits):
        print(f"x{i:02}")
        print(f"y{i:02}")
        values[f"x{i:02}"] = (x >> i) & 1
        values[f"y{i:02}"] = (y >> i) & 1

    return run_logic(values, gates)

def run_logic(values:dict[str,int], gates:list[Gate]) -> int:
    remaining_gates = gates.copy()
    while len(remaining_gates) > 0:
        for gate in remaining_gates.copy():
            if gate.input1 in values and gate.input2 in values:
                if gate.gate == "AND":
                    values[gate.output] = values[gate.input1] & values[gate.input2]
                elif gate.gate == "OR":
                    values[gate.output] = values[gate.input1] | values[gate.input2]
                elif gate.gate == "XOR":
                    values[gate.output] = values[gate.input1] ^ values[gate.input2]
                else:
                    raise Exception(f"Unknown gate: {gate.gate}")
                remaining_gates.remove(gate)

    result = 0
    for gate_name in values.keys():
        if gate_name.startswith("z"):
            result += values[gate_name] << int(gate_name[1:])
    return result


def solve_part_1(values:dict[str,int], gates:list[Gate]) -> int:
    return run_logic(values, gates)

def get_test_pair_sets(gate_indexes:list[int], layers=4):
    test_pair_sets = set()
    for pair in combinations(gate_indexes, 2):
        pair = tuple(pair)
        if layers > 1:
            sub_indexes = gate_indexes.copy()
            sub_indexes.remove(pair[0])
            sub_indexes.remove(pair[1])
            sub_test_sets = get_test_pair_sets(sub_indexes, layers=layers-1)

            for sub_test_set in sub_test_sets:
                unsorted_test_pair_set = [pair]
                unsorted_test_pair_set.extend(sub_test_set)
                test_pair_set = tuple(unsorted_test_pair_set)
                test_pair_sets.add(test_pair_set)

        else:
            test_pair_sets.add((pair,))

    return list(test_pair_sets)
    

def solve_part_2(values, gates):
    vlen = len(gates)
    print(comb(vlen, 2) * comb(vlen-2,2) * comb(vlen-4,2) * comb(vlen-6,2))

    gate_indexes = [i for i in range(len(gates))]
    print(len(get_test_pair_sets(gate_indexes)))
    return ""

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--example", action="store_true")
    args = parser.parse_args()

    values, gates = get_puzzle_input(use_example=args.example)
    answer_1 = solve_part_1(values, gates)
    print(f"Part 1: {answer_1}")

    values, gates = get_puzzle_input(use_example=args.example)
    answer_2 = solve_part_2(values, gates)
    print(f"Part 2: {answer_2}")
