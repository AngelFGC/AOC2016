import curses
import itertools
import re

# RE: (.)(.)\2\1 <-- Match ABBA
# RE: \[.*(.)(.)\2\1.*\] <-- Match ABBA inside brackets

def sample() -> list():
    return """abba[mnop]qrst
abcd[bddb]xyyx
aaaa[qwer]tyui
ioxxoj[asdfgh]zxcvbn
abcd[aabddbxx]xyyx
aba[bab]xyz
xyx[xyx]xyx
aaa[kek]eke
zazbz[bzb]cdb""".splitlines()

def read() -> list():
    with open("inputs/day07.txt", mode="+r", encoding="utf-8") as f:
        return f.read().splitlines()

def part1(win, vis=False):
    #inpt = sample()
    inpt = read()

    cnt = 0
    abbaRE = re.compile(r"(\w)(\w)\2\1")
    abbaSBRE = re.compile(r"\[\w*(\w)(\w)\2\1\w*\]")

    for line in inpt:
        abbas = abbaRE.findall(line)
        abbasBad = abbaSBRE.findall(line)
        isAbbas = any(x!=y for x,y in abbas)
        isAbbasBad = any(x!=y for x,y in abbasBad)
        if isAbbas and not isAbbasBad:
            cnt += 1
    
    print(cnt)

def part2(win, vis=False):
    inpt = read()
    cnt = 0

    hyperdiv = re.compile(r"\[\w*\]")
    avapatt = re.compile(r"(?=(\w)(?!\1)(\w)\1)")

    for line in inpt:
        hypernets = ["".join(c) for c in hyperdiv.findall(line)]
        nothypernets = hyperdiv.split(line)

        hn_bab = set()
        for hn in hypernets:
            hn_bab.update((hnb, hna) for hna, hnb in avapatt.findall(hn))

        nhn_aba = set()
        for nhn in nothypernets:
            nhn_aba.update((nhna, nhnb) for nhna, nhnb in avapatt.findall(nhn))

        if not hn_bab.isdisjoint(nhn_aba):
            cnt += 1

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
