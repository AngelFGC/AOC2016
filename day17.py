import curses
import hashlib
from collections import deque
from typing import Tuple

Room = Tuple[int, int]
DIRECTIONS = {
    "U":(0,-1),
    "D":(0,1),
    "L":(-1,0),
    "R":(1,0)
}
DIRKEYS = "UDLR"
def sample() -> str:
    return "ihgpwlah"

def read() -> str:
    with open("inputs/day17.txt", mode="+r", encoding="utf-8") as f:
        return f.read().strip()

def getneighbors(hash:str, curr:Room) -> Tuple[Room]:
    opens = "bcdef"
    x,y = curr
    return tuple(
        (k, (x + DIRECTIONS[k][0], y + DIRECTIONS[k][1])) for i, k in enumerate(DIRKEYS)
        if 0 <= x + DIRECTIONS[k][0] <= 3 and 0 <= y + DIRECTIONS[k][1] <= 3 and hash[i] in opens
    )

def bfs(start:Room, end:Room, key:str):
    # Tuple contents: dist, path, current room, hash obj
    hbase = hashlib.md5()
    hbase.update(bytearray(key, encoding="utf-8"))
    firstup = ("", start, hbase)
    
    q = deque()
    q.append(firstup)

    while q:
        (path, curr, hobj) = q.popleft()
        if curr == end:
            return path
        hashhex = hobj.hexdigest()
        for dir, nextpos in getneighbors(hashhex, curr):
            hobjupd = hobj.copy()
            hobjupd.update(bytearray(dir, encoding="utf-8"))
            q.append((path + dir, nextpos, hobjupd))
    
    return None

def bfs_full(start:Room, end:Room, key:str):
    # Tuple contents: dist, path, current room, hash obj
    hbase = hashlib.md5()
    hbase.update(bytearray(key, encoding="utf-8"))
    firstup = ("", start, hbase)
    
    q = deque()
    q.append(firstup)

    longest = float("-inf")

    while q:
        (path, curr, hobj) = q.popleft()
        if curr == end:
            longest = max(longest, len(path))
            continue
        hashhex = hobj.hexdigest()
        for dir, nextpos in getneighbors(hashhex, curr):
            hobjupd = hobj.copy()
            hobjupd.update(bytearray(dir, encoding="utf-8"))
            q.append((path + dir, nextpos, hobjupd))
    
    return longest

def part1(win, vis=False):
    #inpt = sample()
    inpt = read()

    assert bfs((0, 0), (3,3), "hijkl") is None
    assert bfs((0, 0), (3,3), "ihgpwlah") == "DDRRRD"
    assert bfs((0, 0), (3,3), "kglvqrro") == "DDUDRLRRUDRD"
    assert bfs((0, 0), (3,3), "ulqzkmiv") == "DRURDRUDDLLDLUURRDULRLDUUDDDRR"

    print(bfs((0, 0), (3,3), inpt))

    
def part2(win, vis=False):
    #inpt = sample()
    inpt = read()

    assert bfs_full((0, 0), (3,3), "hijkl") == float("-inf")
    assert bfs_full((0, 0), (3,3), "ihgpwlah") == 370
    assert bfs_full((0, 0), (3,3), "kglvqrro") == 492
    assert bfs_full((0, 0), (3,3), "ulqzkmiv") == 830

    print(bfs_full((0, 0), (3,3), inpt))

if __name__ == "__main__":
    # CURSES
    win = curses.initscr()
    curses.noecho()
    curses.cbreak()
    if curses.has_colors():
        curses.start_color()
    
    #part1(win, vis=True)
    part2(win, vis=True)
