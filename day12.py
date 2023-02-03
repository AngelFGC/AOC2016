import curses
from typing import List, Dict

class CPU(object):

    reg:Dict[str,int]

    def __init__(self) -> None:
        self.reg = {chr(ord("a")+i):0 for i in range(4)}

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

    def run(self, instrlst:List[str]):
        pctr = 0
        while pctr < len(instrlst):
            pctr = pctr + self.execute_instruction(instrlst[pctr])

    def execute_instruction(self, instruction:str) -> int:
        p = instruction.split(" ")
        pctr = 1
        if p[0] == "cpy":
            x, y = p[1:]
            if y not in self.reg:
                raise ValueError()
            elif x.lstrip("-").isnumeric():
                self.reg[y] = int(x)
            elif x in self.reg:
                self.reg[y] = self.reg[x]
            else:
                raise ValueError()
        elif p[0] == "inc":
            x = p[1]
            if x not in self.reg:
                raise ValueError()
            else:
                self.reg[x] += 1
        elif p[0] == "dec":
            x = p[1]
            if x not in self.reg:
                raise ValueError()
            else:
                self.reg[x] -= 1
        elif p[0] == "jnz":
            x, y = p[1:]
            if y.lstrip("-").isnumeric():
                y = int(y)
            elif y in self.reg:
                y = self.reg[y]
            else:
                raise ValueError()
                
            if x.lstrip("-").isnumeric():
                x = int(x)
            elif x in self.reg:
                x = self.reg[x]
            else:
                raise ValueError()

            if x!= 0:
                pctr = y
        
        return pctr

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

def part1(win, vis=False):
    #inpt = sample()
    inpt = read()

    cpu = CPU()
    cpu.run(inpt)
    
    print(cpu.a)

    
    
def part2(win, vis=False):
    #inpt = sample()
    inpt = read()

    cpu = CPU()
    cpu.reg["c"] = 1
    cpu.run(inpt)
    
    print(cpu.a)

if __name__ == "__main__":
    # CURSES
    win = curses.initscr()
    curses.noecho()
    curses.cbreak()
    if curses.has_colors():
        curses.start_color()
    
    part1(win, vis=True)
    part2(win, vis=True)
