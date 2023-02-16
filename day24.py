import curses
import heapq
from collections import deque, namedtuple
from curses import wrapper
from typing import Tuple, Set, Dict, List, Deque

Point = namedtuple("Point", ["x", "y"])
Node = namedtuple("Node", ["src", "dst", "dist"])

def sample() -> str:
    return """###########
#0.1.....2#
#.#######.#
#4.......3#
###########"""

def read() -> str:
    with open("inputs/day24.txt", mode="+r", encoding="utf-8") as f:
        return f.read()

def extract(s:str) -> Tuple[Set[Point], Dict[int,Point]]:
    halls = set()
    mainnodes = dict()

    for y, line in enumerate(s.splitlines()):
        for x, c in enumerate(line):
            if c == "#":
                continue
            halls.add(Point(x,y))
            if c.isnumeric():
                mainnodes[int(c)] = Point(x,y)
    
    return halls, mainnodes

def tsp(graph:Dict[int, dict]):
    allidx = set(graph.keys())
    # Key: ( distance, path as a tuple ) <-- put this in a heap?
    da_heap = [(0, (0,))]

    while da_heap:
        dist, path = heapq.heappop(da_heap)
        if len(path) == len(allidx):
            return dist
        othernodes = allidx.difference(path)
        for x in othernodes:
            heapq.heappush(da_heap, (
                dist + graph[path[-1]][x],
                path + (x,)
            ))

def tsp_cycle_to_zero(graph:Dict[int, dict]):
    allidx = set(graph.keys())
    # Key: ( distance, path as a tuple ) <-- put this in a heap?
    da_heap = [(0, (0,))]

    graph[0][0] = 0

    while da_heap:
        dist, path = heapq.heappop(da_heap)
        if len(path) == len(allidx):
            return dist
        othernodes = allidx.difference(path)
        for x in othernodes:
            heapq.heappush(da_heap, (
                dist - graph[path[-1]][0] + graph[path[-1]][x] + graph[x][0],
                path + (x,)
            ))

def dfs(nodes:Dict[int,Point], pmap:Set[Point], graph:Dict[int, dict]):
    compass = [
        Point(0,1),
        Point(1,0),
        Point(-1,0),
        Point(0,-1)
    ]
    revnodes = {nodes[k]:k for k in nodes}
    for k in nodes:
        start = nodes[k]
        startidx = revnodes[start]
        visited = set()
        q:Deque[Tuple[int, Point]] = deque()
        q.append((0, start))
        visited.add(start)

        while q:
            (current_dist, pnt) = q.popleft()
            for diff in compass:
                newPnt = Point(pnt.x + diff.x, pnt.y + diff.y)
                if newPnt not in visited and newPnt in pmap:
                    visited.add(newPnt)
                    q.append((current_dist + 1, newPnt))
                    if newPnt in revnodes:
                        pntidx = revnodes[newPnt]
                        if pntidx not in graph[startidx]:
                            graph[startidx][pntidx] = current_dist + 1
                            graph[pntidx][startidx] = current_dist + 1


def part1(win):
    #inpt = sample()
    inpt = read()
    pmap, mainPs = extract(inpt)

    graph = {idx:dict() for idx in mainPs}

    dfs(mainPs, pmap, graph)

    print(tsp(graph))
    
def part2(win):
    #inpt = sample()
    inpt = read()
    pmap, mainPs = extract(inpt)

    graph = {idx:dict() for idx in mainPs}

    dfs(mainPs, pmap, graph)

    print(tsp_cycle_to_zero(graph))

if __name__ == "__main__":
    # CURSES
    wrapper(part1)
    wrapper(part2)
