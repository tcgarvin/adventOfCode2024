import argparse
from dataclasses import dataclass
from itertools import combinations
from math import comb
from rich import print
from typing import NamedTuple

#Gate = NamedTuple("Gate", [("input1", str), ("gate", str), ("input2", str), ("output", str)])   

@dataclass
class Wire:
    name: str

_all_wires = {}
def get_wire(name:str) -> Wire:
    if name not in _all_wires:
        _all_wires[name] = Wire(name)
    return _all_wires[name]

@dataclass
class Gate:
    input1: Wire
    gate: str
    input2: Wire
    output: Wire

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
                gates.append(Gate(
                    get_wire(input1), 
                    gate, 
                    get_wire(input2), 
                    get_wire(output))
                )
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
            name1 = gate.input1.name
            name2 = gate.input2.name
            if name1 in values and name2 in values:
                in_value_1 = values[name1]
                in_value_2 = values[name2]
                if gate.gate == "AND":
                    output_value = in_value_1 & in_value_2
                elif gate.gate == "OR":
                    output_value = in_value_1 | in_value_2
                elif gate.gate == "XOR":
                    output_value = in_value_1 ^ in_value_2
                else:
                    raise Exception(f"Unknown gate: {gate.gate}")
                values[gate.output.name] = output_value
                remaining_gates.remove(gate)

    result = 0
    for gate_name in values.keys():
        if gate_name.startswith("z"):
            result += values[gate_name] << int(gate_name[1:])
    return result


def solve_part_1(values:dict[str,int], gates:list[Gate]) -> int:
    return run_logic(values, gates)

def solve_part_2(values, gates):

    for gate in gates:
        # Swap z12 with kth
        if gate.output.name == "z12":
            gate.output = get_wire("kth")
        elif gate.output.name == "kth":
            gate.output = get_wire("z12")
        # Swap z26 with gsd
        elif gate.output.name == "z26":
            gate.output = get_wire("gsd")
        elif gate.output.name == "gsd":
            gate.output = get_wire("z26")

        # Swap z32 with tbt
        elif gate.output.name == "z32":
            gate.output = get_wire("tbt")
        elif gate.output.name == "tbt":
            gate.output = get_wire("z32")

        # Swap vpm with qnf
        elif gate.output.name == "vpm":
            gate.output = get_wire("qnf")
        elif gate.output.name == "qnf":
            gate.output = get_wire("vpm")


    for _ in range(50):
        for i,gate in enumerate(gates):
            if set([gate.input1.name[0], gate.input2.name[0]]) == set("xy"):
                number = gate.input1.name[1:]
                if gate.gate == "XOR":
                    gate.output.name = f"xor{number}"
                elif gate.gate == "AND":
                    gate.output.name = f"and{number}"

        for i, gate in enumerate(gates):
            pair_names = set([gate.input1.name[:3], gate.input2.name[:3]])
            if (pair_names == set(["xor", "and"]) or pair_names == set(["ofb", "xor"])) and gate.gate == "AND":
                numa = int(gate.input1.name[3:])
                numb = int(gate.input2.name[3:])
                level = max(numa, numb)
                if abs(numa - numb) != 1:
                    raise Exception("Found an issue?")
                else:
                    gate.output.name = f"ofa{level:02}"

        for i, gate in enumerate(gates):
            if set([gate.input1.name[:3], gate.input2.name[:3]]) == set(["ofa", "and"]) and gate.gate == "OR":
                numa = int(gate.input1.name[3:])
                numb = int(gate.input2.name[3:])
                level = max(numa, numb)
                if abs(numa - numb) != 0:
                    raise Exception("Found an issue?")
                else:
                    gate.output.name = f"ofb{level:02}"

    with open("analysis.txt", "w") as analysis:
        for gate in gates:
            analysis.write("\t".join([gate.input1.name, gate.gate, gate.input2.name, gate.output.name]) + "\n")

    # Assert each gate name ends in a number, proving consistency
    for gate in gates:
        if not gate.output.name[-2:].isdigit():
            raise Exception("Found an issue?")

    return ",".join(sorted(["z12", "kth", "vpm", "qnf", "z26", "gsd", "z32", "tbt"]))

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
