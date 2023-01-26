import curses
from typing import List
from time import sleep

def sample() -> str:
    # s = "R2, L3" # 5 blocks
    # s = "R2, R2, R2" # 2 blocks
    # s = "R5, L5, R5, R3" # 12 blocks
    s = "R8, R4, R4, R8"

    return s.split(", ")

def read() -> List[str]:
    with open("inputs/day01.txt", mode="+r", encoding="utf-8") as f:
        return f.read().strip().split(", ")

def part1(win, vis=False):
    #inpt = sample()
    inpt = read()
    dirs = [(0,1), (-1,0), (0,-1), (1,0)]
    turns = {"L":1, "R":-1}
    i = 0
    here = (0,0)
    for c in inpt:
        d,n = c[0], int(c[1:])
        i = (i + turns[d]) % 4
        here = tuple(a + b*n for a,b in zip(here, dirs[i]))
        
    print(sum(map(abs,here)))
    
def part2(stdscrn, vis=False):
    # inpt = sample()
    inpt = read()
    dirs = [(0,1), (-1,0), (0,-1), (1,0)]
    turns = {"L":1, "R":-1}
    i = 0
    here = (0,0)
    locations = set()
    locations.add(here)
    found = False
    for c in inpt:
        d,n = c[0], int(c[1:])
        i = (i + turns[d]) % 4
        for _ in range(n):
            here = tuple(a + b for a,b in zip(here, dirs[i]))
            if here in locations:
                print(sum(map(abs,here)))
                found = True
                break
            locations.add(here)
        if found:
            break

if __name__ == "__main__":
    # CURSES
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    if curses.has_colors():
        curses.start_color()
    
    #part1(stdscr, vis=True)
    part2(stdscr, vis=True)
