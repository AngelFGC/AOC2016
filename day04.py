import curses
import re

def sample() -> str:
    return """aaaaa-bbb-z-y-x-123[abxyz]
a-b-c-d-e-f-g-h-987[abcde]
not-a-real-room-404[oarel]
totally-real-room-200[decoy]""".splitlines()

def read() -> str:
    with open("inputs/day04.txt", mode="+r", encoding="utf-8") as f:
        return f.read().splitlines()

def shiftcipher(s:str, seed:int) -> str:
    return "".join(" " if c == "-" else chr(ord("a") + ((ord(c) - ord("a") + seed) % 26)) for c in s).strip()

def decryptroom(room:str) -> tuple:
    patt = r"(\D+)(\d+)\[(\D+)]"
    m = re.match(patt, room)
    if m is None:
        return 0
    else:
        encname = m.group(1)
        roomnum = int(m.group(2))

        return f"{roomnum}: {shiftcipher(encname, roomnum)}"

def checkroom(room:str) -> tuple:
    patt = r"(\D+)(\d+)\[(\D+)]"
    m = re.match(patt, room)
    if m is None:
        return 0
    else:
        encname = m.group(1)
        roomnum = int(m.group(2))
        chksum = m.group(3)

        cnts = [(encname.count(c) + (1000-ord(c))/10000, c) for c in set(encname.replace("-", ""))]
        cnts.sort(reverse=True)
        
        candidate = "".join(c for _, c in cnts)[:5]

        if candidate == chksum:
            return roomnum
        else:
            return 0

def part1(stdscrn, vis=False):
    #inpt = sample()
    inpt = read()
    print(sum(checkroom(l) for l in inpt))

def part2(win, vis=False):
    #inpt = sample()
    inpt = read()
    for l in inpt:
        if checkroom(l):
            decrypted = decryptroom(l)
            if "pole" in decrypted:
                win.addstr(0,0, decrypted + "\n")
                win.getkey()

if __name__ == "__main__":
    # CURSES
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    if curses.has_colors():
        curses.start_color()
    
    part1(stdscr, vis=True)
    part2(stdscr, vis=True)
