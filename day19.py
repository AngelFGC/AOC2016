import curses
import math

from collections import deque
from time import sleep

def printq(q:deque):
    print("\t >> [" + ", ".join(str(c) for c in q) + "]")

def simulateelfindexP1(nelves:int):
    q = deque((i+1,1) for i in range(nelves))
    while len(q) > 1:
        (Lindex, Lpcount) = q.popleft()
        (_, Rpcount) = q.popleft()
        q.append((Lindex, Lpcount + Rpcount))
    
    Findex, Fcount = q.popleft()
    if Fcount != nelves:
        raise ArithmeticError()
    return Findex

def simulateelfindexP2(nelves:int):
    q = deque((i+1,1) for i in range(nelves))
    #printq(q)
    while len(q) > 1:
        rots = len(q) // 2
        q.rotate(-rots)
        (Rindex, Rpcount) = q.popleft()
        q.rotate(rots)
        (Lindex, Lpcount) = q.popleft()
        q.append((Lindex, Lpcount + Rpcount))
        #printq(q)
    
    Findex, Fcount = q.popleft()
    if Fcount != nelves:
        raise ArithmeticError()
    return Findex

def sample() -> int:
    return 5

def read() -> int:
    with open("inputs/day19.txt", mode="+r", encoding="utf-8") as f:
        return int(f.read().strip())

def mathematicalelfindexP1(nelves:int) -> int:
    base = 2**int(math.log2(nelves))
    return 1 + (nelves - base) * 2

def mathematicalelfindexP2(nelves:int) -> int:
    base3 = int(math.log(nelves, 3))

    nextthreshold = 3**(base3+1)
    prevthreshold = 3**(base3)

    testval = (nelves - prevthreshold) % (nextthreshold - prevthreshold)

    if testval == 0:
        testval = nelves
    elif testval > prevthreshold:
        testval = prevthreshold + (testval - prevthreshold) * 2

    return testval

def part1(win, vis=False):
    #inpt = sample()
    inpt = read()

    print(mathematicalelfindexP1(inpt))
    
def part2(win, vis=False):
    #inpt = sample()
    inpt = read()

    print(mathematicalelfindexP2(inpt))

if __name__ == "__main__":
    # CURSES
    win = curses.initscr()
    curses.noecho()
    curses.cbreak()
    if curses.has_colors():
        curses.start_color()
    
    part1(win, vis=True)
    part2(win, vis=True)
