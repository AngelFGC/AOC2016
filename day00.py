import curses

def sample() -> str:
    pass

def read() -> str:
    with open("inputs/day00.txt", mode="+r", encoding="utf-8") as f:
        return f.read()

def part1(stdscrn, vis=False):
    inpt = sample()
    #inpt = read()
    
def part2(stdscrn, vis=False):
    inpt = sample()
    #inpt = read()

if __name__ == "__main__":
    # CURSES
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    if curses.has_colors():
        curses.start_color()
    
    part1(stdscr, vis=True)
    part2(stdscr, vis=True)
