from functools import partial
from typing import List, Dict, Callable, Any, Tuple

Registry = Dict[str,int]

def cpy(x:str, y:str, reg:Dict[str,int]) -> int:
    if y not in reg:
        raise ValueError()
    elif x.lstrip("-").isnumeric():
        reg[y] = int(x)
    elif x in reg:
        reg[y] = reg[x]
    return 1

def inc(x:str, reg:Dict[str,int]) -> int:
    if x in reg:
        reg[x] += 1
    return 1

def dec(x:str, reg:Dict[str,int]) -> int:
    if x in reg:
        reg[x] -= 1
    return 1

def jnz(x:str, y:str, reg:Dict[str,int]) -> int:
    if y.lstrip("-").isnumeric():
        y = int(y)
    elif y in reg:
        y = reg[y]
    else:
        x = "0"
    
    if x.lstrip("-").isnumeric():
        x = int(x)
    elif x in reg:
        x = reg[x]
    else:
        x = 0
    
    return y if x != 0 else 1

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
            
def convert(instrtxt:List[str]) -> List[partial]:
    return [
        getFunct(instr) for instr in instrtxt
    ]

class CPU(object):
    reg:Registry
    instrs:List[partial]

    def __init__(self, instrlst:List[str]) -> None:
        self.reg = {chr(ord("a")+i):0 for i in range(4)}
        self.pctr = 0
        self.instrs = convert(instrlst)

    def restart(self) -> None:
        for k in self.reg:
            self.reg[k] = 0
    
    @property
    def a(self):
        return self.reg["a"]

    @property
    def b(self):
        return self.reg["b"]

    @property
    def c(self):
        return self.reg["c"]

    @property
    def d(self):
        return self.reg["d"]

    @property
    def pctr(self):
        return self.reg["pctr"]
    
    @pctr.setter
    def pctr(self, v:int):
        self.reg["pctr"] = v

    def run(self):
        self.pctr = 0
        while 0 <= self.pctr < len(self.instrs):
            self.pctr = self.pctr + self.execute_instruction(self.instrs[self.pctr])

    def execute_instruction(self, instruction:partial) -> int:
        return instruction(self.reg)

def sample() -> str:
    return """cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a""".splitlines()

def read() -> str:
    with open("inputs/day12.txt", mode="+r", encoding="utf-8") as f:
        return f.read().splitlines()

def part1():
    #inpt = sample()
    inpt = read()

    cpu = CPU(inpt)
    cpu.run()
    
    print(cpu.a)
    
def part2():
    #inpt = sample()
    inpt = read()

    cpu = CPU(inpt)
    cpu.reg["c"] = 1
    cpu.run()
    
    print(cpu.a)

if __name__ == "__main__":
    # CURSES

    part1()
    part2()
