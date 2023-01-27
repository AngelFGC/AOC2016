import curses
import hashlib
import itertools

def sample() -> str:
    return "abc"

def read() -> str:
    with open("inputs/day05.txt", mode="+r", encoding="utf-8") as f:
        return f.read().strip()

def part1(win, vis=False):
    #inpt = sample()
    inpt = read()

    hbase = hashlib.md5()
    hbase.update(bytearray(inpt, encoding="utf-8"))
    pwd = ""
    for c in itertools.count(1):
        win.addstr(0,0, f"Testing: {inpt}{c}\n")
        h = hbase.copy()
        h.update(bytearray(f"{c}", encoding="utf=8"))
        d = h.hexdigest()
        candidate = d
        win.addstr(1,0, f"Hashed: {candidate}\n")
        if candidate[:5] == "0"*5:
            pwd += candidate[5]
            if len(pwd) == 8:
                break
        win.addstr(2,0, f"Pwd: {pwd}\n")
        win.refresh()
    win.addstr(2,0, f"Pwd: {pwd}\n")
    win.refresh()
    win.getkey()
    
def part2(win, vis=False):
    #inpt = sample()
    inpt = read()

    hbase = hashlib.md5()
    hbase.update(bytearray(inpt, encoding="utf-8"))
    pwd = "--------"
    for c in itertools.count(1):
        win.addstr(0,0, f"Testing: {inpt}{c}\n")
        h = hbase.copy()
        h.update(bytearray(f"{c}", encoding="utf=8"))
        d = h.hexdigest()
        candidate = d
        win.addstr(1,0, f"Hashed: {candidate}\n")
        if candidate[:5] == "0"*5:
            idx = candidate[5]
            if idx.isdigit():
                idx = int(idx)
                if idx < 8 and pwd[idx] == "-":
                    pwd = pwd[:idx] + candidate[6] + pwd[idx+1:]
            if pwd.count("-") == 0:
                break
        win.addstr(2,0, f"Pwd: {pwd}\n")
        win.refresh()
    win.addstr(2,0, f"Pwd: {pwd}\n")
    win.refresh()
    win.getkey()

if __name__ == "__main__":
    # CURSES
    win = curses.initscr()
    curses.noecho()
    curses.cbreak()
    if curses.has_colors():
        curses.start_color()
    
    #part1(win, vis=True)
    part2(win, vis=True)
