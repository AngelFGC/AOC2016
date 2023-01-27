import curses

def sample() -> str:
    return """eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar""".splitlines()

def read() -> str:
    with open("inputs/day06.txt", mode="+r", encoding="utf-8") as f:
        return f.read().splitlines()

def part1(win, vis=False):
    #inpt = sample()
    inpt = read()

    rotated = ["".join(inpt[j][i] for j in range(len(inpt))) for i in range(len(inpt[0]))]
    
    counts = [
        sorted(((r.count(c), c) for c in set(r)), reverse=True)[0][1]
        for r in rotated
    ]

    print("".join(str(c) for c in counts))
    
def part2(win, vis=False):
    #inpt = sample()
    inpt = read()

    rotated = ["".join(inpt[j][i] for j in range(len(inpt))) for i in range(len(inpt[0]))]
    
    counts = [
        sorted(((r.count(c), c) for c in set(r)), reverse=False)[0][1]
        for r in rotated
    ]

    print("".join(str(c) for c in counts))

if __name__ == "__main__":
    # CURSES
    win = curses.initscr()
    curses.noecho()
    curses.cbreak()
    if curses.has_colors():
        curses.start_color()
    
    #part1(win, vis=True)
    part2(win, vis=True)
