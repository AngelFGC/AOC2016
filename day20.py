from __future__ import annotations
import curses
from dataclasses import dataclass
from typing import Iterable
from collections import deque

@dataclass(frozen=True)
class intintv(object):
    lb:int
    ub:int

    def isdisjoint(self, other:intintv):
        return (self.ub < other.lb - 1 or self.lb - 1 > other.ub)

    def join(self, other:intintv) -> tuple:
        if self.isdisjoint(other):
            return (self, other)
        else:
            newlb = min(self.lb, other.lb)
            newub = max(self.ub, other.ub)
            return (intintv(newlb, newub),)
    
    def joinwithiterable(self, it:Iterable) -> Iterable:
        joinable = set(v for v in it if not self.isdisjoint(v))
        unjoinable = set(it).difference(joinable)
        base = intintv(self.lb, self.ub)
        for v in joinable:
            base = base.join(v)[0]
        
        unjoinable.add(base)
        return iter(unjoinable)
    
    def __str__(self):
        return f"[{self.lb}, {self.ub}]"
    
    def __repr__(self):
        return f"[{self.lb}, {self.ub}]"

def sample() -> str:
    pass

def read() -> str:
    with open("inputs/day20.txt", mode="+r", encoding="utf-8") as f:
        lines = (line.split("-") for line in f.read().strip().splitlines())
        return [intintv(int(x), int(y)) for x,y in lines]

def part1(win, vis=False):
    #inpt = sample()
    inpt = read()
    intvranges = set()
    intvranges.add(inpt[0])
    for nintv in inpt[1:]:
        intvranges = set(nintv.joinwithiterable(intvranges))

    sortedranges = sorted(intvranges, key=lambda x: x.lb)
    # print("\n".join(str(x) for x in sortedranges))
    # print("-"*10)
    print((sortedranges[0].ub + sortedranges[1].lb)//2)
    
def part2(win, vis=False):
    #inpt = sample()
    inpt = read()
    intvranges = set()
    intvranges.add(inpt[0])
    for nintv in inpt[1:]:
        intvranges = set(nintv.joinwithiterable(intvranges))
    sortedranges = sorted(intvranges, key=lambda x: x.lb)

    cnt = 0
    if sortedranges[0].lb > 0:
        cnt += sortedranges[0].lb
    for i in range(len(sortedranges) - 1):
        left, right = sortedranges[i:i+2]
        cnt += right.lb - left.ub - 1
    if sortedranges[-1].ub < 4294967295:
        cnt += 4294967295 - sortedranges[-1].ub

    print(cnt)

if __name__ == "__main__":
    # CURSES
    win = curses.initscr()
    curses.noecho()
    curses.cbreak()
    if curses.has_colors():
        curses.start_color()
    
    part1(win, vis=True)
    part2(win, vis=True)
