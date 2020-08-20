import numpy as npp
from math import sqrt


def not_empty(s):
    return s and s.strip()


def main():
    boun = npp.empty(100, int)
    nboun = 0
    npoch = npp.empty(10000, int)
    nboun = 2
    boun[1] = 70
    boun[2] = 846
    sideface = open("sideface.dat", "w")
    sidegridt = open("sidegridt.dat", "r")
    sidenpoch = open("sidenpoch.dat", "r")
    sidegridts = npp.empty((1000, 2), float)
    j = 0
    for line in sidegridt.readlines():
        current_line = list(filter(not_empty, line.strip("\n").split(" ")))
        sidegridts[j][0] = current_line[0]
        sidegridts[j][1] = current_line[1]
        j = j + 1
        nb = j
    sideface.write(str(nb))
    d = 0
    sidenpochs = npp.empty(1000, float)
    for line in sidenpoch.readlines():
        current_line = list(filter(not_empty, line.strip("\n").split(" ")))
        sidenpochs[d] = current_line[0]
        d = d + 1
    for i in range(0, nb):
        npoch[i] = sidenpochs[i]
    istart = 0
    for i in range(0, nboun):
        iend = boun[i]
        for j in range(istart, iend - 1):
            k = npoch[j]
            if k != npoch[j + 1]:
                k = 1
            sideface.write(str(j) + " " + str(j + 1) + " " + str(k))
        k = npoch[iend]
        if k != npoch[istart]:
            k = 1
        sideface.write(str(iend) + " " + str(istart) + " " + str(k))
        istart = iend + 1
    sideface.close()
    sidegridt.close()
    sidenpoch.close()
