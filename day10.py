import curses
import re

from collections import deque

def sample() -> list:
    return """value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2""".splitlines()

def read() -> list:
    with open("inputs/day10.txt", mode="+r", encoding="utf-8") as f:
        return f.read().splitlines()

def addToState(repo:dict, key:str, value:int):
    if key not in repo:
        repo[key] = []
    repo[key].append(value)

def executeinstruction(instr:str, state:dict, pending:dict):
    # patt = re.compile(r"(?:bot (\d+) gives low to bot (\d+) and high to bot (\d+))" +
    #         r"|(?:value (\d+) goes to bot (\d+))")
    affected = deque()
    if "goes to" in instr:
        m = re.search(r"value (\d+) goes to bot (\d+)", instr)
        val, dest = [int(c) for c in m.groups()]
        if dest not in state["bot"]:
            state["bot"][dest] = [val]
        else:
            state["bot"][dest].append(val)
            affected.append(dest)
    else:
        m = re.search(r"bot (\d+) gives low to (\w+) (\d+) and high to (\w+) (\d+)", instr)
        src, type1, dest1, type2, dest2 = m.groups()
        src, dest1, dest2 = int(src), int(dest1), int(dest2)
        if src not in state["bot"]:
            state["bot"][src] = list()
        
        if len(state["bot"][src]) < 2:
            pending[src] = (type1, dest1, type2, dest2)
        else:
            state["bot"][src].sort()
            
            if state["bot"][src] == [17, 61]:
                print(src)
            
            addToState(state[type1], dest1, state["bot"][src][0])
            addToState(state[type2], dest2, state["bot"][src][1])

            state["bot"][src].clear()

            if type1 == "bot":
                affected.append(dest1)
            
            if type2 == "bot":
                affected.append(dest2)

    while affected:
        src = affected.popleft()
        if len(state["bot"][src]) == 2 and src in pending:
            type1, dest1, type2, dest2 = pending[src]
            del pending[src]
            state["bot"][src].sort()

            if state["bot"][src] == [17, 61]:
                print(src)

            addToState(state[type1], dest1, state["bot"][src][0])
            addToState(state[type2], dest2, state["bot"][src][1])
            
            state["bot"][src].clear()
            
            if type1 == "bot":
                affected.append(dest1)
            
            if type2 == "bot":
                affected.append(dest2)

def part1(win, vis=False):
    #inpt = sample()
    inpt = read()
    state = {
        "bot": dict(),
        "output": dict()
    }
    pending = dict()

    for instruction in inpt:
        executeinstruction(instruction, state, pending)
    
    print("Done.")

    
def part2(win, vis=False):
    #inpt = sample()
    inpt = read()
    state = {
        "bot": dict(),
        "output": dict()
    }
    pending = dict()

    for instruction in inpt:
        executeinstruction(instruction, state, pending)

    x = 1
    for i in range(3):
        x *= state["output"][i][0]

    print(x)
    print("Done.")

if __name__ == "__main__":
    # CURSES
    win = curses.initscr()
    curses.noecho()
    curses.cbreak()
    if curses.has_colors():
        curses.start_color()
    
    #part1(win, vis=True)
    part2(win, vis=True)
