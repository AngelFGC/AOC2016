import itertools
import re
from copy import deepcopy

from typing import Tuple, List, Dict, Set
from collections import namedtuple

Node = namedtuple("Point", ["x", "y", "size", "used"])

def sample() -> str:
    return """Filesystem            Size  Used  Avail  Use%
/dev/grid/node-x0-y0   10T    8T     2T   80%
/dev/grid/node-x0-y1   11T    6T     5T   54%
/dev/grid/node-x0-y2   32T   28T     4T   87%
/dev/grid/node-x1-y0    9T    7T     2T   77%
/dev/grid/node-x1-y1    8T    0T     8T    0%
/dev/grid/node-x1-y2   11T    7T     4T   63%
/dev/grid/node-x2-y0   10T    6T     4T   60%
/dev/grid/node-x2-y1    9T    8T     1T   88%
/dev/grid/node-x2-y2    9T    6T     3T   66%""".splitlines()

def read() -> List[str]:
    with open("inputs/day22.txt", mode="+r", encoding="utf-8") as f:
        return f.read().splitlines()

def gettuples(lines:List[str]) -> Dict[Tuple, Node]:
    nodedict = dict()
    rescan = re.compile(r"node\-x(\d+)\-y(\d+)\W+(\d+)T\W+(\d+)T")
    for line in lines:
        m = rescan.search(line)
        if m is not None:
            x,y,size,used = tuple(int(c) for c in m.groups())
            nodedict[(x,y)] = Node(x, y, size, used)
    return nodedict

def getViablePairs(nodedict:dict) -> Set[Tuple[Tuple[int], Tuple[int]]]:
    pairs = set()
    for (xa, ya), (xb, yb) in itertools.product(nodedict.keys(), repeat=2):
        nodea, nodeb = nodedict[(xa, ya)], nodedict[(xb, yb)]
        if nodea.used !=0 and nodea != nodeb and nodea.used <= (nodeb.size - nodeb.used):
            pairs.add(((xa, ya), (xb, yb)))
    return pairs

def part1():
    #inpt = sample()
    inpt = read()
    nodedict = gettuples(inpt)
    vpairs = getViablePairs(nodedict)
    print(len(vpairs))

def printpaircountsavail(vpairs):
    # With this, we can tell how many spaces can *receive* data.
    cnts = dict()
    for y in range(31):
        for x in range(31):
            cnt = 0
            for (A, B) in vpairs:
                if (x,y) == B:
                    cnt += 1
            if cnt > 0:
                cnts[(x,y)] = cnt
    print(cnts) # SPOILERS: It's only one

def gettheemptynode(nodedict):
    for k in nodedict:
        if nodedict[k].used == 0:
            return nodedict[k]

def printpuzzle(x, y, emptynode, largenodes):
    ourpos = (0, 0)
    datapos = (0, x-1)
    for yi in range(y):
        line = ""
        for xi in range(x):
            if (xi, yi) == ourpos:
                line += "\u2690"
            elif (xi, yi) == datapos:
                line += "\u272D"
            elif (xi, yi) in largenodes:
                line += "\u2588"
            elif (xi, yi) == (emptynode.x, emptynode.y):
                line += " "
            else:
                #line += "\u254B"
                line += "."
        print(line)

def printpuzzle2(nodedict:dict):
    maxx = max(x for x,_ in nodedict.keys())
    maxy = max(y for _,y in nodedict.keys())

    for y in range(maxy+1):
        line = ""
        for x in range(maxx+1):
            if (x,y) in nodedict:
                if nodedict[(x,y)].used == 0:
                    line += f"__/{nodedict[(x,y)].size:02d} "
                elif nodedict[(x,y)].used > 100:
                    line += "##/## "
                else:
                    line += f"{nodedict[(x,y)].used:02d}/{nodedict[(x,y)].size:02d} "
            else:
                line += f"__/__ "
        print(line)

# Based on this, we can do it by hand.
# This is my process for my own puzzle:

# To get blank over the wall (Manhattan Distances):
# 9 to the left, 12 up
# Continuing:
# 15 up, 26 to the right
# to move the data one space to the left: 1 to the right
# to move it again: 1 down, 3 left, 1 up, 1 right (6 moves)
# we need to do the move it again 29 more times
# Just added them up.

def printpuzzle3(nodedict:dict):
    maxx = max(x for x,_ in nodedict.keys())
    maxy = max(y for _,y in nodedict.keys())

    for y in range(maxy+1):
        line = ""
        for x in range(maxx+1):
            if (x,y) in nodedict:
                if nodedict[(x,y)].used == 0:
                    line += f"_"
                elif nodedict[(x,y)].used > 100:
                    line += "#"
                else:
                    line += f"."
            else:
                line += f"X"
        print(line)

def part2():

    #inpt = sample()
    inpt = read()
    nodedict = gettuples(inpt)
    printpuzzle2(nodedict)
    printpuzzle3(nodedict)

if __name__ == "__main__":
    #part1()
    part2()
