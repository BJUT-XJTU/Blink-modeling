from math import sqrt, asin

import numpy as npp


def not_empty(s):
    return s and s.strip()

pmax = 100000
emax = 200000
bmax = 50000
fmin = 10 * -8
fm2 = 10 * -8

global np, nboun, sidetype, nbs, bounarc, px, py, pstep, bx, by, bs
np = 0
nboun = 0
sidetype = 0
nbs = 0
bounarc = 0
px = npp.empty(bmax, float)
py = npp.empty(bmax, float)
pstep = npp.empty(bmax, float)
bx = npp.empty(bmax, float)
by = npp.empty(bmax, float)
bs = npp.empty(bmax, float)

global gx, gy, gcx, gcy, gcr, x, y, xce, yce
gx = npp.empty(3, float)
gy = npp.empty(3, float)
gcx = 0.00
gcy = 0.00
gcr = 0.00
x = 0.00
y = 0.00
xce = 0.00
yce = 0.00

global bgnp, bgne, bgstep, bgpx, bgpy, bgcx, bgcy, bgcr, bgnod, bgnoe
bgnp = 0
bgne = 0
bgpx = npp.empty(pmax, float)
bgpy = npp.empty(pmax, float)
bgstep = npp.empty(pmax, float)
bgnod=npp.empty((3, emax), int)
bgnoe=npp.empty((3, emax), int)
bgcx= npp.empty(emax, float)
bgcy= npp.empty(emax, float)
bgcr= npp.empty(emax, float)


def arcscatter(x0, y0, x1, y1, arc):
    # include 't0.inc'
    pmax = 100000
    emax = 200000
    bmax = 50000
    fmin = 10 * -8
    fm2 = 10 * -8

    ee = 0
    x0=0.00
    y0=0.00
    x1=0.00
    y1=0.00
    arcxy = 0.00
    arc0=0.00
    arc=0.00
    arcstep = 0.00
    background_grid()
    arcstep = asin(1.0)*10
    arc0 = 0.0
    np = 1
    nbs = 1
    px[np] = x0
    py[np] = y0
    x = px[np]
    y = py[np]
    search_boun(x, y, ee, arcxy)
    pstep[np] = 0
    arc0 = arc0 + arcxy
    while True:
        if (arc - arc0) <= 0:
            arc0 = arc
            x = x1
            y = y1
            search_boun(x, y, ee, arcxy)
            if (arcxy * 1.5) > (arc0 - pstep[np]):
                break
        elif (arc - arc0) < arcxy:
            arc0 = (arc + arc0 - arcxy) / 2
            transfer_xy(arc0)
            search_boun(x, y, ee, arcxy)
        else:
            transfer_xy(arc0)
            search_boun(x, y, ee, arcxy)
        if (arcxy * 1.5) <= (arc0 - pstep[np]):
            arc0 = arc0 - arcxy * 0.5
        else:
            np = np + 1
            px[np] = x
            py[np] = y
            pstep[np] = arc0
            arc0 = arc0 + arcxy
    np = np + 1
    px[np] = x1
    py[np] = y1
    pstep[np] = arc


# *****************************************
def background_grid():
    # include 't0.inc'
    pmax = 100000
    emax = 200000
    bmax = 50000
    fmin = 10 * -8
    fm2 = 10 * -8

    i = 0
    j = 0
    bgnod = open("bgnod_02.dat", "r")
    bgnoe = open("bgnoe.dat", "r")
    bggridt = open("bggridt_02.dat", "r")
    bgstepp = open("bgstep.dat", "r")
    bgnods = npp.empty((100, 3), float)
    i = 0
    for line in bgnod.readlines():
        current_line = list(filter(not_empty, line.strip("\n").split(" ")))
        bgnods[i][0] = current_line[0]
        bgnods[i][1] = current_line[1]
        bgnods[i][2] = current_line[2]
        i += 1
        bgne = i
    j = 0
    for line in bggridt.readlines():
        current_line = list(filter(not_empty, line.strip("\n").split(" ")))
        bgpx[j] = current_line[0]
        bgpy[j] = current_line[1]
        j += 1
        bgnp = j
    bgsteps = npp.empty(100, float)
    z = 0
    for line in bgstepp.readlines():
        current_line = list(filter(not_empty, line.strip("\n").split(" ")))
        bgsteps[z] = current_line[0]
        z += 1
    for i in range(0, bgnp):
        bgstep[i] = bgsteps[i]
    for i in range(0, bgne):
        bgnod[i][0] = bgnods[i][0]
        bgnod[i][1] = bgnods[i][1]
        bgnod[i][2] = bgnods[i][2]
    bgnoes = npp.empty((100, 3), float)
    d = 0
    for line in bgstepp.readlines():
        current_line = list(filter(not_empty, line.strip("\n").split(" ")))
        bgnoes[d][0] = current_line[0]
        bgnoes[d][1] = current_line[1]
        bgnoes[d][2] = current_line[2]
        d += 1
    for i in range(0, bgne):
        bgnoe[i, 0] = bgnoes[i][0]
        bgnoe[i, 1] = bgnoes[i][1]
        bgnoe[i, 2] = bgnoes[i][2]
    bgnod.close()
    bgnoe.close()
    bggridt.close()
    bgstepp.close()
    for i in range(0, bgne):
        for j in range(0, 3):
            gx[j] = bgpx[bgnod[j, i]]
            gy[j] = bgpy[bgnod[j, i]]
        circumcircle()
        bgcx[i] = gcx
        bgcy[i] = gcy
        bgcr[i] = gcr


# ***********************************
def search_boun(xx, yy, result, step):
    # include 't0.inc'
    pmax = 100000
    emax = 200000
    bmax = 50000
    fmin = 10 * -8
    fm2 = 10 * -8

    xx = 0.00
    yy = 0.00
    step=0.00
    result=0
    i = 0
    j = 0
    k = 0
    nbg = npp.empty(3, int)
    emin=0
    arr = npp.empty((3, 3), float)
    dcp = 0.00
    bulk = npp.empty(3, float)
    v1 = 0.00
    v2 = 0.00
    v4 = 0.00
    vmin=0.00
    vol = np.empty(3, float)
    vmin = 1.0
    emin = 0
    result = 0
    for i in range(bgne, 0, -1):
        nbg[0] = bgnoe[0, i]
        nbg[1] = bgnoe[1, i]
        nbg[2] = bgnoe[2, i]
        gcx = bgcx[i]
        gcy = bgcy[i]
        gcr = bgcr[i]
        dcp = sqrt((xx - gcx) ** 2 + (yy - gcy) ** 2)
        for k in range(0, 3):
            for j in range(0, 3):
                arr[0, j] = 1
                arr[1, j] = bgpx[bgnod[j, i]]
                arr[2, j] = bgpy[bgnod[j, i]]
            arr[1, k] = xx
            arr[2, k] = yy
            det(arr, 3, bulk[k])
        v1 = bulk[0] + bulk[1] + bulk[2]
        v2 = abs(bulk[0]) + abs(bulk[1]) + abs(bulk[2])
        v4 = (v2 - v1) / v1
        if v4 < (10 ** -1):
            if vmin > v4:
                vmin = v4
                emin = i
                vol[0] = bulk[0]
                vol[1] = bulk[1]
                vol[2] = bulk[2]
    if emin == 0:
        print("error")
        return
    v1 = vol[0] + vol[1] + vol[2]
    v2 = abs(vol[0]) + abs(vol[1]) + abs(vol[2])
    v4 = v1 + v2
    step = 0
    for k in range(0, 3):
        vol[k] = (vol[k] + abs(vol[k])) / v4
        step = step + bgstep[bgnod[k, emin]] * vol[k]
    result = emin


# *****************************************


def circumcircle():
    # include 't0.inc'
    pmax = 100000
    emax = 200000
    bmax = 50000
    fmin = 10 * -8
    fm2 = 10 * -8

    i = 0
    arr = npp.empty((2, 2), float)
    ver = npp.empty(2, float)
    verx = npp.empty(2, float)
    x1 = 0.00
    x2 = 0.00
    x3 = 0.00
    r1 = 0.00
    r2 = 0.00
    r3 = 0.00
    for i in range(0, 2):
        arr[i, 0] = gx[i] - gx[2]
        arr[i, 1] = gy[i] - gy[2]
        ver[i] = 0.5 * (arr[i, 0] ** 2 + arr[i, 1] ** 2)
    axeqb(arr, ver, 2, verx)
    gcx = verx[0] + gx[2]
    gcy = verx[1] + gy[2]
    x1 = gx[0] - gcx
    x2 = gy[0] - gcy
    x3 = sqrt(x1 * x1 + x2 * x2)
    r1 = x3
    x1 = gx[1] - gcx
    x2 = gy[1] - gcy
    x3 = sqrt(x1 * x1 + x2 * x2)
    r2 = x3
    r3 = sqrt(verx[0] ** 2 + verx[1] ** 2)
    gcr = (r1 + r2 + r3) / 3


# *************************************
def axeqb(arr1, verb1, num, verx1):
    num = 0
    arr1=npp.empty((num, num), float)
    arr = npp.empty((num, num), float)
    verb1=npp.empty(num, float)
    verx1=npp.empty(num, float)
    verb = npp.empty(num, float)
    verx = npp.empty(num, float)
    i = 0
    j = 0
    k = 0
    real_1 = 0.0
    real_2 = 0.0
    for i in range(0, num):
        for j in range(0, num):
            arr[i, j] = arr1[i, j]
    verb[i] = verb1[i]

    for i in range(0, num - 1):
        real_1 = arr[i, i]
        for j in range(i + 1, num):
            if abs(arr[j, i]) > abs(real_1):
                for k in range(i, num):
                    real_1 = arr[i, k]
                    arr[i, k] = arr[j, k]
                    arr[j, k] = real_1
                real_1 = verb[i]
                verb[i] = verb[j]
                verb[j] = real_1
            real_1 = arr[i, i]
        real_1 = arr[i, i]
        arr[i, i] = 1.0
        if abs(real_1) < (10 ** -8):
            print("error1:3 point in 1 line")
            print(i, real_1)
            k = input()
            return
        for j in range(i + 1, num):
            arr[i, j] = arr[i, j] / real_1
        verb[i] = verb[i] / real_1
        for j in range(i + 1, num):
            real_2 = arr[j, i]
            arr[j, i] = 0.0
            for k in range(i + 1, num):
                arr[j, k] = arr[j, k] - real_2 * arr[i, k]
            verb[j] = verb[j] - real_2 * verb[i]
    if abs(arr[num, num]) < (10 ** -8):
        print("error2:3 point in 1 line")
        print(arr[num, num])
        k = input()
        return
    verx[num] = verb[num] / arr[num, num]
    for i in range(num - 1, 0, -1):
        verx[i] = verb[i]
        for j in range(num, i, -1):
            verx[i] = verx[i] - arr[i, j] * verx[j]
    for i in range(0, num):
        verx1[i] = verx[i]


# ****************************************
def det(matri, num, det_matri):
    num=0
    matri = npp.empty((num, num), float)
    matrix = npp.empty((num, num), float)
    i = 0
    j = 0
    k = 0
    sign_1 = 0
    det_matri=0.00
    det_matrix = 0.00
    real_1 = 0.00
    real_2 = 0.00
    for i in range(0, num):
        for j in range(0, num):
            matrix[j, i] = matri[i, j]
    det_matrix = 1
    sign_1 = 1
    for i in range(0, num - 1):
        real_1 = matrix[i, i]
        for j in range(i + 1, num):
            if abs(matrix[j, i]) > abs(real_1):
                for k in range(i, num):
                    real_1 = matrix[i, k]
                    matrix[i, k] = matrix[j, k]
                    matrix[j, k] = real_1
                real_1 = matrix[i, i]
                sign_1 = sign_1 * (-1)
        real_1 = matrix[i, i]
        if abs(real_1) < (10 ** -15):
            det_matri = 0.0
            return
        matrix[i, i] = 1.0
        det_matrix = det_matrix * real_1
        for j in range(i + 1, num):
            real_2 = matrix[j, i] / real_1
            matrix[j, i] = 0.0
            for k in range(i + 1, num):
                matrix[j, k] = matrix[j, k] - real_2 * matrix[i, k]
    det_matrix = det_matrix * matrix[num, num] * sign_1
    det_matri = det_matrix


# *********************************
def loadboun(filename):
    # include 't0.inc'
    pmax = 100000
    emax = 200000
    bmax = 50000
    fmin = 10 * -8
    fm2 = 10 * -8

    i = 0
    fil = open(filename, "r")
    for line in fil.readlines():
        current_line = list(filter(not_empty, line.strip("\n").split(" ")))
        bx[i] = current_line[0]
        by[i] = current_line[1]
        bs[i] = current_line[2]
    fil.close()


# ***********************************

def transfer_xy(arc):
    # include 't0.inc'
    pmax = 100000
    emax = 200000
    bmax = 50000
    fmin = 10 * -8
    fm2 = 10 * -8

    nboun = 0
    nbs = 0
    arc = 0.00
    ratio = 0.00
    i = 0
    n = 0
    # sidetype=1 离散形式的边界
    if sidetype == 1:
        if bs[nbs] >= arc:
            n = 1
            for i in range(nbs, 0, -1):
                if bs[i] < arc:
                    n = i
                    break
        elif bs[nbs] < arc:
            n = nboun
            for i in range(nbs, nboun):
                if bs[i] >= arc:
                    n = i - 1
                    break
        nbs = n
        if n == 1 or n == nboun:
            x = bx[n]
            y = by[n]
        else:
            ratio = (arc - bs[n]) / (bs[n + 1] - bs[n])
            x = bx[n] + ratio * (bx[n + 1] - bx[n])
            y = by[n] + ratio * (by[n + 1] - by[n])
        # sidetype=2 连续边界，函数形式
    elif sidetype == 2:
        arc_to_xy(arc, x, y)
    elif sidetype == 3:
        arcn_to_xy(arc, x, y)
