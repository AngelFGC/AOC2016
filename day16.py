import curses

def sample() -> tuple:
    return 20, "10000"

def read() -> tuple:
    with open("inputs/day16.txt", mode="+r", encoding="utf-8") as f:
        x, y = f.read().strip().split(",")
        return int(x), y

def dragoncurve(a:str) -> str:
    b = "".join("1" if c == "0" else "0" for c in a[::-1])
    return f"{a}0{b}"

def checksum(s:str) -> str:
    while len(s) % 2 == 0:
        itr = (s[i:i+2] for i in range(0, len(s)-1, 2))
        s = "".join(
            "1" if s[i] == s[i+1] else "0"
            for i in range(0, len(s)-1, 2)
        )
    return s

def part1(win, vis=False):
    #inpt = sample()
    inpt = read()
    size, state = inpt
    
    while len(state) < size:
        state = dragoncurve(state)

    state = state[:size]
    while len(state) % 2 == 0:
        state = checksum(state)
    
    print(state)
    
def part2(win, vis=False):
    #inpt = sample()
    inpt = read()
    size, state = 35651584, inpt[1]

    while len(state) < size:
        state = dragoncurve(state)
        
    state = state[:size]
    while len(state) % 2 == 0:
        state = checksum(state)
    
    print(state)

if __name__ == "__main__":
    # CURSES
    win = curses.initscr()
    curses.noecho()
    curses.cbreak()
    if curses.has_colors():
        curses.start_color()
    
    part1(win, vis=True)
    part2(win, vis=True)
