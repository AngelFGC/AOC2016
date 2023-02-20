from day23 import CPU2, getFunct
from curses import wrapper
from typing import List, Dict, Any
from functools import partial

Registry2 = Dict[str, Any]

def printStatus3(stdscrn, reg:Dict[str,int]):
    stdscrn.clear()
    stdscrn.addstr("=================\n")
    stdscrn.addstr("| CPU SIMULATOR |\n")
    stdscrn.addstr("=================\n")
    stdscrn.addstr(f"PC = {reg['pctr']}\n")
    stdscrn.addstr("Registers:\n")
    for i,c in [(i,chr(ord("a")+i)) for i in range(4)]:
        stdscrn.addstr(f"  {c} = {reg[c]}\n")
    #stdscrn.addstr(f"  sgnl (last 5) = {reg['sgnl'][-5:] if len(reg['sgnl']) > 5 else reg['sgnl']}\n")
    stdscrn.addstr(f"  sgnl (last 5) = {reg['sgnl']}\n")
    stdscrn.refresh()

def out(x:str, reg:Dict[str,int]) -> int:
    if x.lstrip("-").isnumeric():
        x = int(x)
    elif x in reg:
        x = reg[x]
    else:
        return 1

    reg["sgnl"] += str(x)

    return 1

def sum(x:str, y:str, reg:Dict[str,int]) -> int:
    if y.lstrip("-").isnumeric():
        y = int(y)
    elif y in reg:
        y = reg[y]
    else:
        return 1
    
    if x in reg:
        reg[x] = reg[x] + y
    
    return 1

def getFunct3(instr:str) -> partial:
    p = instr.split(" ")
    if p[0] == "out":
        x = p[1]
        return partial(out, x)
    elif p[0] == "sum":
        x, y = p[1:]
        return partial(sum, x, y)
    else:
        return getFunct(instr)

def convert(instrtxt:List[str]) -> List[partial]:
    return [
        getFunct3(instr.strip()) for instr in instrtxt if instr.strip()[0] != "#"
    ]

class CPU3(CPU2):
    reg:Registry2
    def __init__(self, instrlst: List[str]) -> None:
        super().__init__(instrlst)
        self.reg["sgnl"] = ""
        self.instrs = convert(instrlst)
    
    @property
    def sgnl(self) -> str:
        return self.reg["sgnl"]

    def restart(self) -> None:
        super().restart()
        self.reg["sgnl"] = ""

    def runUI(self, stdscrn):
        self.pctr = 0
        printStatus3(stdscrn, self.reg)
        while 0 <= self.pctr < len(self.instrs):
            next_pctr = self.pctr + self.execute_instruction(self.instrs[self.pctr])
            self.pctr = next_pctr
            printStatus3(stdscrn, self.reg)

    def runUIuntil(self, stdscrn, sgnlcom:str) -> bool:
        self.pctr = 0
        printStatus3(stdscrn, self.reg)
        while (0 <= self.pctr < len(self.instrs) 
                and len(self.sgnl) < len(sgnlcom)
                and sgnlcom.startswith(self.sgnl)):
            next_pctr = self.pctr + self.execute_instruction(self.instrs[self.pctr])
            self.pctr = next_pctr
            printStatus3(stdscrn, self.reg)
        return self.sgnl.startswith(sgnlcom) or sgnlcom.startswith(self.sgnl)

def read() -> str:
    with open("inputs/day25_mod.txt", mode="+r", encoding="utf-8") as f:
        return f.read().splitlines()

def part1(stdscrn):
    inpt = read()
    cpu = CPU3(inpt)

    found = False
    i = 0
    while not found:
        i += 1
        cpu.restart()
        cpu.reg["a"] = i
        found = cpu.runUIuntil(stdscrn, "01"*10)

    print(i)
    
def part2(win, vis=False):
    #inpt = sample()
    inpt = read()

if __name__ == "__main__":
    # CURSES
    wrapper(part1)
    #wrapper(part2)
