import curses
import itertools

def sample() -> str:
    pass

def read() -> str:
    with open("inputs/day03.txt", mode="+r", encoding="utf-8") as f:
        return [tuple(int(x) for x in line.strip().split()) for line in f]

def istriangle(candidate:tuple) -> bool:
    return all(a+b > c for a,b,c in itertools.permutations(candidate, 3))

def part1(stdscrn, vis=False):
    #inpt = sample()
    inpt = read()
    
    total = sum(istriangle(c) for c in inpt)
    print(total)
    print(len(inpt))
    
def part2(stdscrn, vis=False):
    #inpt = sample()
    inpt = read()
    newTs = []

    for i in range(0, len(inpt), 3):
        for j in range(3):
            newTs.append(tuple(inpt[i+k][j] for k in range(3)))
    
    total = sum(istriangle(c) for c in newTs)
    print(total)
    print(len(newTs))

if __name__ == "__main__":
    # CURSES
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    if curses.has_colors():
        curses.start_color()
    
    part1(stdscr, vis=True)
    part2(stdscr, vis=True)
