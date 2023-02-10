import curses
import re
from collections import deque

def sample() -> str:
    return """swap position 4 with position 0
swap letter d with letter b
reverse positions 0 through 4
rotate left 1 step
move position 1 to position 4
move position 3 to position 0
rotate based on position of letter b
rotate based on position of letter d""".splitlines()

def read() -> str:
    with open("inputs/day21.txt", mode="+r", encoding="utf-8") as f:
        return f.read().strip().splitlines()

def swappos(pwd:list, X:int, Y:int) -> list:
    return [
        pwd[Y] if i == X
        else pwd[X] if i == Y
        else v
        for i,v in enumerate(pwd)
    ]

def swaplet(pwd:list, X:str, Y:str) -> list:
    posX = pwd.index(X)
    posY = pwd.index(Y)
    return swappos(pwd, posX, posY)

def rotate(pwd:list, rotLeft:bool, X:int) -> list:
    n = len(pwd)
    if rotLeft:
        X = -X
    return [
        pwd[(i - X) % n]
        for i in range(n)
    ]

def rotatebased(pwd:list, X:str) -> list:
    idxofX = pwd.index(X)
    rots = 1 + idxofX + (1 if idxofX >= 4 else 0)
    return rotate(pwd, False, rots)

def rotaterebased(pwd:list, X:str) -> list:
    revrotsfor8 = {1:0, 3:1, 5:2, 7:3, 2:4, 4:5, 6:6, 0:7}
    idxofX = pwd.index(X)
    oldidx = revrotsfor8[idxofX]
    rots = idxofX - oldidx
    
    return rotate(pwd, rots > 0, abs(rots))

def reversepos(pwd:list, X:int, Y:int) -> list:
    return (
        pwd[:X] +
        list(reversed(pwd[X:Y+1])) +
        pwd[Y+1:]
    )

def move(pwd:list, X:int, Y:int) -> list:
    newList = []
    if Y > X:
        newList = (
            pwd[:X] +
            rotate(pwd[X:Y+1], True, 1) +
            pwd[Y+1:]
        )
    elif X > Y:
        newList = (
            pwd[:Y] +
            rotate(pwd[Y:X+1], False, 1) +
            pwd[X+1:]
        )
    else:
        newList = pwd
    
    return newList

def scramble(pwd:str, instrs:list) -> str:
    pwd = list(pwd)
    getter = re.compile(r"\b(\d+|\w)\b")
    for inst in instrs:
        params = getter.findall(inst)
        if "swap pos" in inst:
            x,y = [int(c) for c in params]
            pwd = swappos(pwd, x, y)
        elif "swap let" in inst:
            x,y = params
            pwd = swaplet(pwd, x, y)
        elif "rotate based" in inst:
            x = params[0]
            pwd = rotatebased(pwd, x)
        elif "rotate" in inst:
            rotLeft = "left" in inst
            x = int(params[0])
            pwd = rotate(pwd, rotLeft, x)
        elif "reverse" in inst:
            x,y = [int(c) for c in params]
            pwd = reversepos(pwd, x, y)
        elif "move" in inst:
            x,y = [int(c) for c in params]
            pwd = move(pwd, x, y)
    return "".join(pwd)

def unscramble(pwd:str, instrs:list) -> str:
    pwd = list(pwd)
    getter = re.compile(r"\b(\d+|\w)\b")
    for inst in instrs[::-1]:
        params = getter.findall(inst)
        if "swap pos" in inst: #Same
            x,y = [int(c) for c in params]
            pwd = swappos(pwd, x, y)
        elif "swap let" in inst: #Same
            x,y = params
            pwd = swaplet(pwd, x, y)
        elif "rotate based" in inst: #Diff
            x = params[0]
            pwd = rotaterebased(pwd, x)
        elif "rotate" in inst: #Diff
            rotLeft = "left" in inst
            x = int(params[0])
            pwd = rotate(pwd, not rotLeft, x)
        elif "reverse" in inst: #Diff? Not really
            x,y = [int(c) for c in params]
            pwd = reversepos(pwd, x, y)
        elif "move" in inst: #Diff
            x,y = [int(c) for c in params]
            pwd = move(pwd, y, x)
    return "".join(pwd)

def part1(win, vis=False):
    inpt = sample()
    
    assert scramble("abcde", inpt) == "decab"

    inpt = read()

    print(scramble("abcdefgh", inpt))

    
def part2(win, vis=False):
    inpt = read()

    # acfebdgh is wrong
    # fdhgacbe
    print(unscramble("fbgdceah", inpt))

if __name__ == "__main__":
    # CURSES
    win = curses.initscr()
    curses.noecho()
    curses.cbreak()
    if curses.has_colors():
        curses.start_color()
    
    part1(win, vis=True)
    part2(win, vis=True)
