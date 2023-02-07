import curses
import itertools
import re

def sample() -> str:
    return """Disc #1 has 5 positions; at time=0, it is at position 4.
Disc #2 has 2 positions; at time=0, it is at position 1.""".splitlines()

def read() -> str:
    with open("inputs/day15.txt", mode="+r", encoding="utf-8") as f:
        return f.read().splitlines()

def getdiscs(lines:list) -> list:
    crexp = re.compile(r"(\d+) positions; at time=0, it is at position (\d+)")
    return [
        tuple(int(c) for c in crexp.search(l).groups())
        for l in lines if crexp.search(l) is not None
    ]

def part1(win, vis=False):
    #inpt = sample()
    inpt = read()
    discs = getdiscs(inpt)
    # These are the indices that guarantee a perfect drop.
    findices = tuple(
        (posn - i - 1) % posn
        for i, (posn, pos0) in enumerate(discs)
    )
    for tj in itertools.count(0):
        tindices  = tuple(
            (pos0 + tj) % posn
            for posn, pos0 in discs
        )
        if findices == tindices:
            break
    
    print(tj)
    
def part2(win, vis=False):
    #inpt = sample()
    inpt = read()
    discs = getdiscs(inpt)
    discs.append((11, 0))
    # These are the indices that guarantee a perfect drop.
    findices = tuple(
        (posn - i - 1) % posn
        for i, (posn, _) in enumerate(discs)
    )
    for tj in itertools.count(0):
        tindices  = tuple(
            (pos0 + tj) % posn
            for posn, pos0 in discs
        )
        if findices == tindices:
            break
    
    print(tj)

if __name__ == "__main__":
    # CURSES
    win = curses.initscr()
    curses.noecho()
    curses.cbreak()
    if curses.has_colors():
        curses.start_color()
    
    part1(win, vis=True)
    part2(win, vis=True)
