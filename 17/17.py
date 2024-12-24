import argparse
import re
from typing import NamedTuple
from rich import print

INPUT_PATTERN = re.compile("""
    Register[ ]A:[ ](?P<register_a>\d+)[\n]
    Register[ ]B:[ ](?P<register_b>\d+)[\n]
    Register[ ]C:[ ](?P<register_c>\d+)[\n]
    [\n]
    Program:[ ](?P<program>[0-9,]+)[\n]
""", re.MULTILINE | re.VERBOSE)

ProgramInput = NamedTuple("ProgramInput", register_a=int, register_b=int, register_c=int, program=list[int])

def get_puzzle_input(use_example=False):
    input_filename = "example2.txt" if use_example else "input.txt"
    puzzle_input = None
    with open(input_filename) as input_txt:
        match = INPUT_PATTERN.fullmatch(input_txt.read())
        puzzle_input = ProgramInput(
            int(match["register_a"]), 
            int(match["register_b"]), 
            int(match["register_c"]), 
            [int(x) for x in match["program"].split(",")]
        )
    return puzzle_input


class Computer:
    def __init__(self, register_a: int, register_b: int, register_c: int, program: list[int]):
        self._register_a = register_a
        self._register_b = register_b
        self._register_c = register_c
        self._instruction_pointer = 0
        self._program = program
        self.output = []

    def execute(self):
        while self._instruction_pointer < len(self._program):
            instruction = self._program[self._instruction_pointer]
            if instruction == 0:
                self._adv()
            elif instruction == 1:
                self._bxl()
            elif instruction == 2:
                self._bst()
            elif instruction == 3:
                self._jnz()
            elif instruction == 4:
                self._bxc()
            elif instruction == 5:
                self._out()
            elif instruction == 6:
                self._bdv()
            elif instruction == 7:
                self._cdv()

    def _resolve_combo_operator(self, operator:int) -> int:
        result = None
        if operator in [0,1,2,3]:
            result = operator
        elif operator == 4:
            result = self._register_a
        elif operator == 5:
            result = self._register_b
        elif operator == 6:
            result = self._register_c
        elif operator == 7:
            raise Exception("Reserved.")
        return result

    def _adv(self):
        combo_operator = self._program[self._instruction_pointer + 1]
        operand = self._resolve_combo_operator(combo_operator)
        result = self._register_a // (2 ** operand)
        self._register_a = result
        self._instruction_pointer += 2

    def _bxl(self):
        operand = self._program[self._instruction_pointer + 1]
        result = self._register_b ^ operand
        self._register_b = result
        self._instruction_pointer += 2

    def _bst(self):
        combo_operator = self._program[self._instruction_pointer + 1]
        operand = self._resolve_combo_operator(combo_operator)
        result = operand % 8
        self._register_b = result
        self._instruction_pointer += 2

    def _jnz(self):
        if self._register_a == 0:
            self._instruction_pointer += 2
            return
        
        operand = self._program[self._instruction_pointer + 1]
        self._instruction_pointer = operand

    def _bxc(self):
        result = self._register_b ^ self._register_c
        self._register_b = result
        self._instruction_pointer += 2

    def _out(self):
        combo_operator = self._program[self._instruction_pointer + 1]
        operand = self._resolve_combo_operator(combo_operator)
        result = operand % 8
        self.output.append(result)
        self._instruction_pointer += 2

    def _bdv(self):
        combo_operator = self._program[self._instruction_pointer + 1]
        operand = self._resolve_combo_operator(combo_operator)
        result = self._register_a // (2 ** operand)
        self._register_b = result
        self._instruction_pointer += 2

    def _cdv(self):
        combo_operator = self._program[self._instruction_pointer + 1]
        operand = self._resolve_combo_operator(combo_operator)
        result = self._register_a // (2 ** operand)
        self._register_c = result
        self._instruction_pointer += 2


def solve_part_1(puzzle_input: ProgramInput):
    computer = Computer(
        puzzle_input.register_a, 
        puzzle_input.register_b, 
        puzzle_input.register_c, 
        puzzle_input.program
    )
    computer.execute()
    return ",".join([str(x) for x in computer.output])

def one_loop(a:int):
    out = ((a % 8) ^ 3 ^ (a >> ((a % 8) ^ 5))) % 8
    a = a >> 3
    return a, out

def solve_part_1_alt(puzzle_input: ProgramInput):
    if puzzle_input.program != [2,4,1,5,7,5,1,6,0,3,4,0,5,5,3,0]:
        print("This solution is only valid for the full program, not any example")
        return ""
    a = puzzle_input.register_a
    assert puzzle_input.register_b == 0
    assert puzzle_input.register_c == 0
    assert puzzle_input.program == [2,4,1,5,7,5,1,6,0,3,4,0,5,5,3,0]

    output = []
    while a != 0:
        a, out = one_loop(a)
        output.append(out)
    return output

def _find_smallest_a(a_prefix:int, target_program: list[int]) -> int:
    if len(target_program) == 0:
        return a_prefix

    target = target_program[-1]
    found_smallest_a = False
    smallest_a = -1
    for candidate_extension in range(0,8):
        a = (a_prefix << 3) + candidate_extension
        _, out = one_loop(a)
        if out == target:
            print(f"{a:b}")
            smallest_a = _find_smallest_a(a, target_program[:-1])
            if smallest_a != -1:
                break

    return smallest_a
    
def solve_part_2(puzzle_input:ProgramInput):
    if puzzle_input.program != [2,4,1,5,7,5,1,6,0,3,4,0,5,5,3,0]:
        print("This solution is only valid for the full program, not any example")
        return ""

    a_prefix = _find_smallest_a(0, puzzle_input.program)

    return a_prefix


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--example", action="store_true")
    args = parser.parse_args()

    puzzle_input = get_puzzle_input(use_example=args.example)

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    alt_answer_1 = solve_part_1_alt(puzzle_input)
    print(f"Part 1 (alternative): {alt_answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")
