import curses
import hashlib
import itertools

def sample() -> str:
    return "abc"

def read() -> str:
    with open("inputs/day14.txt", mode="+r", encoding="utf-8") as f:
        return f.read().strip()

def threeinarow(hashstr:str):
    for i, c in enumerate(hashstr[:-2]):
        if hashstr[i:i+3] == c*3:
            return c
    return ""

def fiveinarow(hashstr:str, c:str):
    for i, d in enumerate(hashstr[:-4]):
        if c == d and hashstr[i:i+5] == c*5:
            return True
    return False

def genhashes(salt:str):
    hbase = hashlib.md5()
    hbase.update(bytearray(salt, encoding="utf-8"))
    for i in itertools.count():
        h = hbase.copy()
        h.update(bytearray(f"{i}", encoding="utf=8"))
        d = h.hexdigest()
        yield i, d

def genhashes2(salt:str):
    hbase = hashlib.md5()
    hbase.update(bytearray(salt, encoding="utf-8"))
    for i in itertools.count():
        h = hbase.copy()
        h.update(bytearray(f"{i}", encoding="utf=8"))
        d = h.hexdigest()
        for _ in range(2016):
            h2 = hashlib.md5()
            h2.update(bytearray(d, encoding="utf-8"))
            d = h2.hexdigest()
        yield i, d

def part1(win, vis=False):
    inpt = sample()
    #inpt = read()
    candidates = dict()
    keys = set()

    for i, d in genhashes(inpt):
        todel = set()
        for k in candidates:
            candidates[k][1] += 1
            if candidates[k][1] > 1000:
                todel.add(k)
            elif fiveinarow(d, candidates[k][0]):
                keys.add(k)
                if len(keys) == 64:
                    print(i - candidates[k][1])
                    break
                todel.add(k)
                try:
                    win.addstr(f"({i:06d}) {k} \u2192 {candidates[k][1]:04d} \u2192 {d}\n")
                except:
                    win.move(0,0)
                    win.addstr(f"({i:06d}) {k} \u2192 {candidates[k][1]:04d} \u2192 {d}\n")
        for k in todel:
            del candidates[k]

        win.refresh()
        c = threeinarow(d)

        if c:
            candidates[d] = [c, 0]
        
        if len(keys) >= 64:
            break
    
def part2(win, vis=False):
    #inpt = sample()
    inpt = read()
    candidates = dict()
    keys = set()

    for i, d in genhashes2(inpt):
        todel = set()
        for k in candidates:
            candidates[k][1] += 1
            if candidates[k][1] > 1000:
                todel.add(k)
            elif fiveinarow(d, candidates[k][0]):
                keys.add(k)
                if len(keys) == 64:
                    print(i - candidates[k][1])
                    break
                todel.add(k)
                try:
                    win.addstr(f"({i:06d}) {k} \u2192 {candidates[k][1]:04d} \u2192 {d}\n")
                except:
                    win.move(0,0)
                    win.addstr(f"({i:06d}) {k} \u2192 {candidates[k][1]:04d} \u2192 {d}\n")
        for k in todel:
            del candidates[k]

        win.refresh()
        c = threeinarow(d)

        if c:
            candidates[d] = [c, 0]
        
        if len(keys) >= 64:
            break

if __name__ == "__main__":
    # CURSES
    win = curses.initscr()
    curses.noecho()
    curses.cbreak()
    if curses.has_colors():
        curses.start_color()
    
    #part1(win, vis=True)
    part2(win, vis=True)
