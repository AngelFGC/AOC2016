import curses
import itertools
import heapq
from dataclasses import dataclass, field
from typing import List, Tuple

def sample() -> Tuple[int]:
    return (10, 7, 4)

def read() -> int:
    with open("inputs/day13.txt", mode="+r", encoding="utf-8") as f:
        return tuple(int(x) for x in f.read().split(","))

def isopen(n:int, x:int, y:int) -> bool:
    return (
        sum(c == "1" for c in bin((x + y)**2 + 3*x + y + n)[2:]) % 2 == 0
        if x >= 0 and y >= 0 else False
    )

def getneighbors(n:int, x:int, y:int) -> List[Tuple[int]]:
    return [
        (x + dx, y + dy) for dx, dy in [(0,1),(0,-1),(1,0),(-1,0)]
        if isopen(n, x + dx, y + dy)
    ]

def dijkstra(start:Tuple[int], end:Tuple[int], n:int):
    dist = dict()
    prev = dict()
    nodes = dict()
    prev[start] = None
    dist[start] = 0

    theheap = [(0, start)]
    visited = set()

    while theheap:
        d, curr = heapq.heappop(theheap)
        x, y = curr

        if (x,y) == end:
            break

        for xn, yn in getneighbors(n, x, y):
            if (xn, yn) not in visited:
                alt = d + 1
                if (xn, yn) in dist:
                    oldd = dist[(xn, yn)]
                    idx = theheap.index((oldd, (xn, yn)))
                    if alt < oldd:
                        dist[(xn, yn)]
                        prev[(xn, yn)] = (x,y)
                        theheap[idx] = (alt, (xn, yn))
                else:
                    dist[(xn, yn)] = alt
                    prev[(xn, yn)] = (x,y)
                    theheap.append((alt, (xn, yn)))
        heapq.heapify(theheap)
        visited.add((x,y))
    return dist, prev

def dijkstra2(start:Tuple[int], n:int):
    dist = dict()
    prev = dict()
    nodes = dict()
    prev[start] = None
    dist[start] = 0

    theheap = [(0, start)]
    visited = set()

    while theheap:
        d, curr = heapq.heappop(theheap)
        x, y = curr

        if d == 50:
            continue
        elif d > 50:
            break

        for xn, yn in getneighbors(n, x, y):
            if (xn, yn) not in visited:
                alt = d + 1
                if (xn, yn) in dist:
                    oldd = dist[(xn, yn)]
                    idx = theheap.index((oldd, (xn, yn)))
                    if alt < oldd:
                        dist[(xn, yn)]
                        prev[(xn, yn)] = (x,y)
                        theheap[idx] = (alt, (xn, yn))
                else:
                    dist[(xn, yn)] = alt
                    prev[(xn, yn)] = (x,y)
                    theheap.append((alt, (xn, yn)))
        heapq.heapify(theheap)
        visited.add((x,y))
    return dist, prev

def part1(win, vis=False):
    # inpt = sample()
    inpt = read()
    n, xf, yf = inpt
    x0, y0 = 1, 1
    dist, prev = dijkstra((x0, y0), (xf, yf), n)
    print(dist[(xf, yf)])
    
def part2(win, vis=False):
    #inpt = sample()
    inpt = read()
    n, xf, yf = inpt
    x0, y0 = 1, 1
    dist, prev = dijkstra2((x0, y0), n)
    print(sum(dist[k] <= 50 for k in dist))

if __name__ == "__main__":
    # CURSES
    win = curses.initscr()
    curses.noecho()
    curses.cbreak()
    if curses.has_colors():
        curses.start_color()
    
    #part1(win, vis=True)
    part2(win, vis=True)
