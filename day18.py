import curses

def sample() -> list:
    return [0 if c == "." else 1 for c in ".^^.^.^^^^"]

def read() -> list:
    with open("inputs/day18.txt", mode="+r", encoding="utf-8") as f:
        return [0 if c == "." else 1 for c in f.read().strip()]

TRAPGEN = {
    (0, 0, 0):0,
    (0, 0, 1):1,
    (0, 1, 0):0,
    (0, 1, 1):1,
    (1, 0, 0):1,
    (1, 0, 1):0,
    (1, 1, 0):1,
    (1, 1, 1):0
}

def getNextState(state:list) -> list:
    nextStateChecker = [
        (
            0 if i == 0 else state[i - 1],
            tile,
            0 if i == len(state) - 1 else state[i + 1]
        )
        for i, tile in enumerate(state)
    ]

    return [TRAPGEN[t] for t in nextStateChecker]

def getRepr(state:list):
    return "".join("^" if c else "." for c in state)

def runcheck(startState:list, nits:int, print=False) -> int:
    state = startState
    n = len(state)
    safestates = n - sum(state)
    if print:
        print(getRepr(state))
    for i in range(nits):
        state = getNextState(state)
        if print:
            print(getRepr(state))
        safestates += n - sum(state)
    return safestates

def part1(win, vis=False):
    #inpt = sample()
    inpt = read()

    assert runcheck(sample(), 9) == 38

    print(runcheck(inpt, 39))
    
def part2(win, vis=False):
    #inpt = sample()
    inpt = read()

    print(runcheck(inpt, 400000 - 1))

if __name__ == "__main__":
    # CURSES
    win = curses.initscr()
    curses.noecho()
    curses.cbreak()
    if curses.has_colors():
        curses.start_color()
    
    part1(win, vis=True)
    part2(win, vis=True)
