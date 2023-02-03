import curses
import itertools
from collections import deque

import heapq

# Evens are gens, Odds are

def sample() -> list:
    return eval("""(1,
        (1, 3),
        (2,),
        (4,),
        tuple()
    )""".replace("  ", "").replace("\n", ""))

def read() -> str:
    with open("inputs/day11.txt", mode="+r", encoding="utf-8") as f:
        txt = f.read().replace("\n","")
        v = eval(txt)
        return v

def final(state:tuple) -> bool:
    return all(not f for f in state[1:4])

def valid(state:tuple) -> bool:
    for floor in state[1:]:
        gens = {x-1 for x in floor if x%2 == 0}
        batts = {x for x in floor if x%2 == 1}

        if len(gens) == 0 or len(batts) == 0:
            continue

        powered_gens = gens & batts
        unshielded_batts = batts - gens

        if powered_gens and unshielded_batts:
            return False
        
    return True

 
def getHash(state:tuple):

    return (state[0],) + tuple((len(f), sum(x % 2 == 1 for x in f)) for f in state[1:])
    
    perfloor_hash = [
        f"[{len(f)},{sum(x for x in f if x % 2 == 1)}]"
        for f in state[1:]
    ]
    return f"{state[0]}," + ",".join(perfloor_hash)

def genmoves(state:tuple):
    f = state[0]
    elems = state[f]
    for combo in itertools.chain(
        itertools.combinations(elems, 2),
        itertools.combinations(elems, 1)
    ):
        if len(combo) == 2:
            x, y = sorted(combo)
            if (x % 2) + (y % 2) == 1:
                if y > x + 1 or x % 2 == 0:
                    continue
        for newf in [f+1, f-1]:
            if 0 < newf < len(state):
                newstate = [newf,
                    tuple(),
                    tuple(),
                    tuple(),
                    tuple()
                ]
                x = tuple()
                
                newstate[f] = tuple(x for x in state[f] if x not in combo)
                for i in range(1,5):
                    if i != f:
                        newstate[i] = tuple(x for x in state[i])
                
                newstate[newf] = tuple(sorted(newstate[newf] + combo))
                newstate = tuple(newstate) 

                if len(state[1]) == 0 and len(newstate[1]) != 0:
                    continue
                elif len(state[1]) == len(newstate[1]) == 0:
                    if len(state[2]) == 0 and len(newstate[2]) != 0:
                        continue

                if valid(newstate):
                    yield newstate

def h(state:tuple):
    d = 0
    for i, r in enumerate(state[1:]):
        d += len(r) * (3 - i)
    return d

def getDistance(cameFrom:dict, current:tuple):
    dist = 0
    while current in cameFrom:
        current = cameFrom[current]
        dist += 1
    return dist

def solve_astar(start:tuple, win):
    cameFrom = dict()
    gScore = dict()
    gScore[start] = 0
    fScore = dict()
    fScore[start] = h(start)
    opensetQ = [(fScore[start], start)]
    openset = {getHash(start)}

    win.addstr(0, 0, f"Open Set: \t{len(openset)}\n")
    win.addstr(1, 0, f"Current Dist: \t{opensetQ[0][0]}\n")
    win.refresh()
    while opensetQ:
        h_dist, current = heapq.heappop(opensetQ)
        openset.remove(getHash(current))
        
        if final(current):
            return getDistance(cameFrom, current)
        
        for neighbor in genmoves(current):
            diff = abs(h(neighbor) - h(current))
            nhash = getHash(neighbor)
            tentative_gscore = gScore.setdefault(current, float("+inf")) + diff
            if tentative_gscore < gScore.setdefault(neighbor, float("+inf")):
                cameFrom[neighbor] = current
                gScore[neighbor] = tentative_gscore
                fScore[neighbor] = tentative_gscore + h(neighbor)
                
                if nhash not in openset:
                    heapq.heappush(opensetQ, (fScore[neighbor], neighbor))
                    openset.add(nhash)
        win.addstr(0, 0, f"Open Set: \t{len(openset)}\n")
        win.addstr(1, 0, f"Current Dist: \t{opensetQ[0][0]}\n")
        win.refresh()
    
    return None

def part1(win, vis=False):
    #inpt = sample()
    inpt = read()
    print(solve_astar(inpt, win))

def part2(win, vis=False):
    #inpt = sample()
    inpt = list(read())
    inpt[1] = inpt[1] + (11,12,13,14)
    inpt = tuple(inpt)
    print(solve_astar(inpt, win))

if __name__ == "__main__":
    # CURSES
    win = curses.initscr()
    curses.noecho()
    curses.cbreak()
    if curses.has_colors():
        curses.start_color()
    
    #part1(win, vis=True)
    part2(win, vis=True)
