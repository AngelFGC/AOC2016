import curses
import itertools
import re

from time import sleep

def sample() -> tuple:
    return 7, 3, """rect 3x2
rotate column x=1 by 1
rotate row y=0 by 4
rotate column x=1 by 1
""".splitlines()

def display(win, w:int, h:int, pixels:set, latest:str) -> None:
    win.addstr(0,0, f"Last instr: {latest}\n")
    for x,y in itertools.product(range(w), range(h)):
        if (x,y) in pixels:
            win.addstr(y+1,x, "#")
        else:
            win.addstr(y+1,x, ".")
    #win.addstr("\n\n")
    win.refresh()

def rect(pixels:set, A:int, B:int, w:int, h:int):
    for x,y in itertools.product(range(min(A,w)), range(min(B,h))):
        pixels.add((x,y))

def rotaterow(pixels:set, A:int, B:int, w:int, h:int):
    if 0 <= A < h:
        rowA = {(x, y) for (x, y) in pixels if y==A}
        pixels.difference_update(rowA)
        rowA = {((x + B) % w, y) for (x, y) in rowA}
        pixels.update(rowA)

def rotatecol(pixels:set, A:int, B:int, w:int, h:int):
    if 0 <= A < w:
        colA = {(x, y) for (x, y) in pixels if x==A}
        pixels.difference_update(colA)
        colA = {(x, (y + B) % h) for (x, y) in colA}
        pixels.update(colA)

def execinstr(instr:str, pixels:set, w:int, h:int):
    if "rect" in instr:
        m = re.search(r"(\d+)x(\d+)", instr)
        if m:
            A, B = int(m[1]), int(m[2])
            rect(pixels, A, B, w, h)
    else:
        m = re.search(r"(\d+) by (\d+)", instr)
        if m: 
            A, B = int(m[1]), int(m[2])
            if "rotate row" in instr:
                rotaterow(pixels, A, B, w, h)
            elif "rotate column" in instr:
                rotatecol(pixels, A, B, w, h)

def read() -> str:
    with open("inputs/day08.txt", mode="+r", encoding="utf-8") as f:
        return 50, 6, f.read().splitlines()

def part1(win, vis=False):
    fps = 1/12
    #w, h, inpt = sample()
    w, h, inpt = read()
    pixels = set()

    display(win, w, h, pixels, "--")
    sleep(fps)

    for i in inpt:
        execinstr(i, pixels, w, h)
        display(win, w, h, pixels, i)
        sleep(fps)
    win.addstr("\n\nDone.\n")
    win.addstr(f"Pixels lit: {len(pixels)}\n")
    win.getkey()

if __name__ == "__main__":
    # CURSES
    win = curses.initscr()
    curses.noecho()
    curses.cbreak()
    if curses.has_colors():
        curses.start_color()
    
    part1(win, vis=True)
