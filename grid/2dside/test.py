import numpy as npp


def not_empty(s):
    return s and s.strip()


aaa = npp.empty((50, 3), int)
fil = open("bgnod.dat", "r")
i=0
for line in fil.readlines():
    current_line = list(filter(not_empty, line.strip("\n").split(" ")))
    if i > 0:
        aaa[i][0]= current_line[0]
        aaa[i][1] = current_line[1]
        aaa[i][2] = current_line[2]
    else:
        uu=current_line[0]
    i=i+1
print(aaa)
print(uu)
