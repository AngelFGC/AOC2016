import curses

from curses import wrapper
from typing import List
from day12 import *

from collections import deque

def printStatus(stdscrn, reg:Dict[str,int]):
    stdscrn.clear()
    stdscrn.addstr("=================\n")
    stdscrn.addstr("| CPU SIMULATOR |\n")
    stdscrn.addstr("=================\n")
    stdscrn.addstr(f"PC = {reg['pctr']}\n")
    stdscrn.addstr("Registers:\n")
    for i,c in [(i,chr(ord("a")+i)) for i in range(4)]:
        stdscrn.addstr(f"  {c} = {reg[c]}\n")
    stdscrn.refresh()

def tgl(x:str, reg:Dict[str,int], instrList:List[partial]) -> int:
    pctr = reg["pctr"]
    if x.lstrip("-").isnumeric():
        x = int(x) + pctr
        print(reg[x])
    elif x in reg:
        x = reg[x] + pctr
    else:
        x = -1

    if 0 <= x < len(instrList):
        instrList[x] = getSwap(instrList[x])

    return 1

"""
Solving this problem can be hard: the original asm code contains
Loops that can be simplified with other operations.
Trying to identify those loops via code is *wasteful*.
However, a person can identify those by sight, so it is possible
to replace them with an equivalent operation:
instead of so much addition, we can do a MULtiplication.

However, adding multiplication means changing the number of operations
in the code, which screws up some of the jumps. So we need to pad
the code with dummy Not-Operations (NOPs)
"""
def nop(x:str, reg:Dict[str,int]) ->int:
    return 1

def mul(x:str, y:str, reg:Dict[str,int]) -> int:
    if y.lstrip("-").isnumeric():
        y = int(y)
    elif y in reg:
        y = reg[y]
    else:
        return 1
    
    if x in reg:
        reg[x] = reg[x] * y
    
    return 1

def getSwap(foriginal:partial) -> partial:
    if len(foriginal.args) == 1:
        if foriginal.func == inc:
            return partial(dec, *foriginal.args)
        else:
            return partial(inc, *foriginal.args)
    elif len(foriginal.args) == 2:
        if foriginal.func == jnz:
            return partial(cpy, *foriginal.args)
        else:
            return partial(jnz, *foriginal.args)

def getFunct(instr:str) -> partial:
    p = instr.split(" ")
    if p[0] == "cpy":
        x, y = p[1:]
        return partial(cpy, x, y)
    elif p[0] == "inc":
        x = p[1]
        return partial(inc, x)
    elif p[0] == "dec":
        x = p[1]
        return partial(dec, x)
    elif p[0] == "jnz":
        x, y = p[1:]
        return partial(jnz, x, y)
    elif p[0] == "tgl":
        x = p[1]
        return partial(tgl, x)
    elif p[0] == "mul":
        x, y = p[1:]
        return partial(mul, x, y)
    elif p[0] == "nop":
        return partial(nop, "@")

def convert(instrtxt:List[str]) -> List[partial]:
    return [
        getFunct(instr.strip()) for instr in instrtxt if instr.strip()[0] != "#"
    ]

class CPU2(CPU):
    def __init__(self, instrlst:List[str]) -> None:
        self.reg = {chr(ord("a")+i):0 for i in range(4)}
        self.pctr = 0
        self.instrs = convert(instrlst)

    def execute_instruction(self, instruction:partial) -> int:
        return (
            instruction(self.reg, self.instrs)
            if instruction.func == tgl
            else instruction(self.reg)
        )
    
    def runUI(self, stdscrn):
        self.pctr = 0
        printStatus(stdscrn, self.reg)
        while 0 <= self.pctr < len(self.instrs):
            next_pctr = self.pctr + self.execute_instruction(self.instrs[self.pctr])
            self.pctr = next_pctr
            printStatus(stdscrn, self.reg)

def sample() -> str:
    return """cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a""".splitlines()

def read() -> str:
    with open("inputs/day23_MOD.txt", mode="+r", encoding="utf-8") as f:
        return f.read().splitlines()

def part1(stdscrn):
    #inpt = sample()
    inpt = read()

    cpu = CPU2(inpt)
    cpu.reg["a"] = 7
    
    cpu.runUI(stdscrn)
    #cpu.run()
    
    print(cpu.a)
    
def part2(stdscrn):
    #inpt = sample()
    inpt = read()

    cpu = CPU2(inpt)
    cpu.reg["a"] = 12
    
    cpu.runUI(stdscrn)
    #cpu.run()
    
    print(cpu.a)

if __name__ == "__main__":
    # CURSES
        
    wrapper(part1)
    wrapper(part2)
