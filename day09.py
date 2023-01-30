import curses
import re

def sample() -> str:
    #return "ADVENT" # "ADVENT"
    #return "A(1x5)BC" # ABBBBBC
    #return "(3x3)XYZ" # XYZXYZXYZ
    #return "A(2x2)BCD(2x2)EFG" # ABCBCDEFEFG
    #return "(6x1)(1x3)A" # (1x3)A
    #return "X(8x2)(3x3)ABCY" # X(3x3)ABC(3x3)ABCY, p2 length is XABCABCABCABCABCABCY
    # FOR PART 2
    #return "(27x12)(20x12)(13x14)(7x10)(1x12)A" # length: 241920
    return "(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN" # length: 445

def read() -> str:
    with open("inputs/day09.txt", mode="+r", encoding="utf-8") as f:
        return f.read().strip()

def decompresslen(comp:str):
    if not comp:
        return 0
    else:
        lensum = 0
        m = re.search(r"\((\d+)x(\d+)\)", comp)
        while m is not None:
            x, y = m.groups()
            x, y = int(x), int(y)
            lensum += m.start()
            lensum += decompresslen(comp[m.end():m.end() + x]) * y
            comp = comp[m.end() + x:]
            m = re.search(r"\((\d+)x(\d+)\)", comp)
        return lensum + len(comp)

def part1(win, vis=False):
    #inpt = sample()
    inpt = read()
    p = re.compile(r"\((\d+)x(\d+)\)")
    comp = inpt
    lensum = 0
    m = p.search(comp)

    while m is not None:
        x, y = m.groups()
        x, y = int(x), int(y)
        lensum += m.start() + x*y
        comp = comp[m.end() + x:]
        m = p.search(comp)
    lensum += len(comp)
    print(lensum)


def part2(win, vis=False):
    #inpt = sample()
    inpt = read()
    print(decompresslen(inpt))

if __name__ == "__main__":
    # CURSES
    win = curses.initscr()
    curses.noecho()
    curses.cbreak()
    if curses.has_colors():
        curses.start_color()
    
    #part1(win, vis=True)
    part2(win, vis=True)
