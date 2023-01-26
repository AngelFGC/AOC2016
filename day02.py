import curses

def sample() -> str:
    return """ULL
RRDDD
LURDL
UUUUD""".splitlines()

KEYPAD1 = """123
456
789"""
KEYPAD2 = """  1
 234
56789
 ABC
  D"""

def read() -> str:
    with open("inputs/day02.txt", mode="+r", encoding="utf-8") as f:
        return f.read().splitlines()

def getKeypad(kp:list) -> dict:
    keypad = dict()
    dirs = [
        ("U", -1, 0),
        ("D", 1, 0),
        ("L", 0, -1),
        ("R", 0, 1)
    ]
    for i,l in enumerate(kp):
        for j,c in enumerate(l):
            if c == " ":
                continue
            for d, x, y in dirs:
                i2, j2 = i + x, j + y
                if (
                    0 <= i2 < len(kp) and
                    0 <= j2 < len(kp[i2])
                ):
                    if kp[i2][j2] != " ":
                        keypad.setdefault(c, dict())[d] = kp[i2][j2]
    return keypad

def part1(stdscrn, vis=False):
    #inpt = sample()
    inpt = read()

    keypad = getKeypad(KEYPAD1.splitlines())

    code = ""
    key = "5"
    for line in inpt:
        for c in line:
            key = keypad[key][c] if c in keypad[key] else key
        code = code + key
    
    print(code)
    
def part2(stdscrn, vis=False):
    #inpt = sample()
    inpt = read()
    
    keypad = getKeypad(KEYPAD2.splitlines())

    code = ""
    key = "5"
    for line in inpt:
        for c in line:
            key = keypad[key][c] if c in keypad[key] else key
        code = code + key
    
    print(code)

if __name__ == "__main__":
    # CURSES
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    if curses.has_colors():
        curses.start_color()
    
    part1(stdscr, vis=True)
    part2(stdscr, vis=True)
