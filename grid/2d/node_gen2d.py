from math import sqrt

import numpy as npp
pmax=100000
emax=200000
delmax=1000
bmax=2000
fmin=10**-8
fm2=10**-8

global np, ne, nsearch, px, py, cx, cy, cr, nod, noe, epoch, ipx, ipy, centx, centy, length
np=0
ne=0
nsearch=0
px = npp.empty(pmax, float)
py = npp.empty(pmax, float)
ipx = npp.empty(4, float)
ipy = npp.empty(4, float)
centx=0.0
centy=0.0
length=0.0
nod=npp.empty((3, emax), int)
noe=npp.empty((3, emax), int)
epoch=npp.empty(emax, int)
cx=npp.empty(emax, float)
cy=npp.empty(pmax, float)
cr=npp.empty(pmax, float)

global gx, gy, gcx, gcy, gcr, x, y, xce, yce
gx=npp.empty(3, float)
gy=npp.empty(3, float)
gcx=0.0
gcy=0.0
gcr=0.0
x=0.0
y=0.0
xce=0.0
yce=0.0

global ndel, edel, neibn
ndel=0
edel=npp.empty(delmax, int)
neibn=npp.empty(delmax, int)

global eos, side, nb, nps
eos = npp.empty((2, bmax), int)
side = npp.empty((3, bmax), int)
nb=0
nps=0

global newnp, ecrit, eop, bgeop, pstep
newnp=0
ecrit=npp.empty(emax, int)
eop=npp.empty(pmax, int)
bgeop=npp.empty(pmax, int)
pstep=npp.empty(pmax, float)

global bgnp, bgne, bgstep, bgfail, bgsearch, bgepoch
global bgpx, bgpy, bgcx, bgcy, bgcr, bgnod, bgnoe
bgnp=0
bgne=0
bgfail=0
bgsearch=0
bgpx=npp.empty(pmax, float)
bgpy=npp.empty(pmax, float)
bgstep=npp.empty(pmax, float)
bgnod=npp.empty((3, emax), int)
bgnoe=npp.empty((3, emax), int)
bgepoch=npp.empty(emax, int)
bgcx=npp.empty(emax, float)
bgcy=npp.empty(emax, float)
bgcr=npp.empty(emax, float)

def advance_front():
    # include "t0.inc"
    pmax = 100000
    emax = 200000
    delmax = 1000
    bmax = 2000
    fmin = 10 ** -8
    fm2 = 10 ** -8

    # global np, ne, nsearch, px, py, cx, cy, cr, nod, noe, epoch, ipx, ipy, centx, centy, length
    # px = np.empty(pmax, float)
    # py = np.empty(pmax, float)
    # ipx = np.empty(4, float)
    # ipy = np.empty(4, float)
    # centx = 0.0
    # centy = 0.0
    # length = 0.0
    # nod = np.empty((3, emax), int)
    # noe = np.empty((3, emax), int)
    # epoch = np.empty(emax, int)
    # cx = np.empty(emax, float)
    # cy = np.empty(pmax, float)
    # cr = np.empty(pmax, float)
    #
    # global gx, gy, gcx, gcy, gcr, x, y, xce, yce
    # gx = np.empty(3, float)
    # gy = np.empty(3, float)
    # gcx = 0.0
    # gcy = 0.0
    # gcr = 0.0
    # x = 0.0
    # y = 0.0
    # xce = 0.0
    # yce = 0.0
    #
    # global ndel, edel, neibn
    # ndel = 0
    # edel = np.empty(delmax, int)
    # neibn = np.empty(delmax, int)
    #
    # global eos, side, nb, nps
    # eos = np.empty((2, bmax), int)
    # side = np.empty((3, bmax), int)
    # nb = 0
    # nps = 0
    #
    # global newnp, ecrit, eop, bgeop, pstep
    # newnp = 0
    # ecrit = np.empty(emax, int)
    # eop = np.empty(pmax, int)
    # bgeop = np.empty(pmax, int)
    # pstep = np.empty(pmax, float)
    #
    # global bgnp, bgne, bgstep, bgfail, bgsearch, bgepoch
    # global bgpx, bgpy, bgcx, bgcy, bgcr, bgnod, bgnoe
    # bgnp = 0
    # bgne = 0
    # bgfail = 0
    # bgsearch = 0
    # bgpx = np.empty(pmax, float)
    # bgpy = np.empty(pmax, float)
    # bgstep = np.empty(pmax, float)
    # bgnod = np.empty((3, emax), int)
    # bgnoe = np.empty((3, emax), int)
    # bgepoch = np.empty(emax, int)
    # bgcx = np.empty(emax, float)
    # bgcy = np.empty(emax, float)
    # bgcr = np.empty(emax, float)

    i = 0
    j = 0
    k = 0
    m = 0
    n = 0
    nei = 0
    ep = 0
    emx = 0
    emn = 0
    bgep = 0
    p = 0
    f1 = 0.0
    f3 = 0.0
    step = 0.0
    xn = 0.0
    yn = 0.0
    vx = 0.0
    vy = 0.0
    lcs = 0.0
    lsp = 0.0
    xx = 0.0
    yy = 0.0
    x1 = 0.0
    x2 = 0.0
    y1 = 0.0
    y2 = 0.0
    pp = np.empty(3, int)
    ee = np.empty(2, int)
    p2 = np.empty(3, int)
    sx = np.empty(3, float)
    sy = np.empty(3, float)
    ss = np.empty(3, float)
    sr = np.empty(3, float)

    f1 = 0.7
    f3 = 0.3
    nsearch = 0
    for i in range(0, ne):
        epoch[i] = 0
    bgsearch = 0
    for i in range(0, bgne):
        bgepoch[i] = 0
    newnp = np
    for i in range(0, ne):
        if ecrit[i] != 1:
            continue
        pp[0] = nod[0, i]
        pp[1] = nod[1, i]
        pp[2] = nod[2, i]
        for j in range(0, 3):
            nei = noe[j, i]
            if nei > 0 and ecrit[nei] != -1:
                continue
            # 该面的内法向量及外界圆心、半径
            m = j + 1
            n = m + 1
            # ？？？
            if m > 3:
                m = m - 3
            if n > 3:
                n = n - 3
            ee[0] = bgeop[pp[m]]
            ee[1] = bgeop[pp[n]]
            yn = px[pp[n]] - px[pp[m]]
            xn = py[pp[m]] - py[pp[n]]
            lsp = sqrt(xn * xn + yn * yn)
            xn = xn / lsp
            yn = yn / lsp
            lcs = (cx[i] - px[pp[n]]) * xn + (cy[i] - py[pp[n]]) * yn
            sx[j] = cx[i] - lcs * xn
            sy[j] = cy[i] - lcs * yn
            sr[j] = sqrt(cr[i] * cr[i] - lcs * lcs)
            emx = max(ee[0], ee[1])
            emn = min(ee[0], ee[1])
            if emx == emn:
                ss[j] = (pstep[pp[0]] + pstep[pp[1]]) / 2.0
            else:
                search_in_bg(sx[j], sy[j], emx, bgep, ss[j])
                if bgep == 0:
                    #  ss(j)=(pstep(pp(1))+pstep(pp(2)))/2.0
                    if nei != 0:
                        print("error:search=0", i, j, nei)
                        bgep = input()
                    else nei==0:
                        search_boun(sx[j], sy[j], bgep, ss[j])
                        if bgep == 0:
                            print("error:search=0", i, j, nei)
                            bgep = input()
            if ss[j] > 3.0 * sr[j]:
                ss[j] = 3.0 * sr[j]
            # 推进的新点坐标及其与该面构成的四面体外心及半径
            xx = sx[j] + ss[j] * xn
            yy = sy[j] + ss[j] * yn
            gcr = 0.5 * ss[j] + 0.5 * sr[j] * sr[j] / ss[j]
            gcx = xx - gcr * xn
            gcy = yy - gcr * yn
            # 以下为该点是否应存在的判定
            lcs = sqrt((gcx - px[pp[j]]) ** 2 + (gcy - py[pp[j]]) ** 2)
            if lcs < gcr:
                continue
            if bgep > 0:
                emx = bgep
            search_in_bg(xx, yy, emx, bgep, step)
            if bgep == 0:
                continue
            lcs = sqrt((xx - px[pp[j]]) ** 2 + (yy - py[pp[j]]) ** 2)
            if lcs < f1 * step:
                continue
            p = newnp + 1
            if p > pmax:
                print("newnp>pmax:", newnp, pmax)
                p = input()
            px[p] = xx
            py[p] = yy
            search_1st(p, i, ep)
            if ep == 0:
                continue
            p2[0] = nod[0, ep]
            p2[1] = nod[1, ep]
            p2[2] = nod[2, ep]
            for k in range(0, 3):
                lcs = sqrt((px[p2[k]] - xx) ** 2 + (py[p2[k]] - yy) ** 2)
                lsp = pstep[p2[k]] * f1
                if lcs < f1 * step and lcs < lsp:
                    p = 0
                    break
            if p == 0:
                continue
            for k in range(0, 3):
                nei = noe[k, ep]
                if nei != 0:
                    continue
                m = k + 1
                n = m + 1
                if m > 3:
                    m = m - 3
                if n > 3:
                    n = n - 3
                vx = py[p2[m]] - py[p2[n]]
                vy = px[p2[n]] - px[p2[m]]
                lsp = sqrt(vx * vx + vy * vy)
                vx = vx / lsp
                vy = vy / lsp
                lsp = abs(vx * (xx - px[p2[n]]) + vy * (yy - py[p2[n]]))
                if lsp < f3 * step:
                    p = 0
                    break
            if p == 0:
                continue
            search_all(p, ep)
            x1 = xx + step * f1
            x2 = xx - step * f1
            y1 = yy + step * f1
            y2 = yy - step * f1
            for k in range(1, ndel):
                for m in range(0, 3):
                    if px[nod[m, edel[k]]] > x1:
                        continue
                    if px[nod[m, edel[k]]] < x2:
                        continue
                    if py[nod[m, edel[k]]] > y1:
                        continue
                    if py[nod[m, edel[k]]] > y2:
                        continue
                    vx = px[nod[m, edel[k]]]
                    vy = py[nod[m, edel[k]]]
                    lcs = sqrt((vx - xx) ** 2 + (vy - yy) ** 2)
                    if lcs < f1 * step:
                        p = 0
                        break
                if p == 0:
                    break
            if p == 0:
                continue
            newnp = newnp + 1
            pstep[newnp] = step
            eop[newnp] = ep
            bgeop[newnp] = bgep

    for i in range(np+1, newnp):
        if eop[i] == 0:
            continue
        for j in range(i+1, newnp):
            if eop[i] == 0:
                continue
            if pstep[j] < pstep[i]:
                xx = px[i]
                px[i] = px[j]
                px[j] = xx
                yy = py[i]
                py[i] = py[j]
                py[j] = yy
                step = pstep[i]
                pstep[i] = pstep[j]
                pstep[j] = step
                ep = eop[i]
                eop[i] = eop[j]
                eop[j] = ep
                bgep = bgeop[i]
                bgeop[i] = bgeop[j]
                bgeop[j] = bgep
        xx = px[i]
        yy = py[i]
        step = pstep[i] * f1
        x1 = xx - step
        x2 = xx + step
        y1 = yy - step
        y2 = yy + step
        for j in range(i+1, newnp):
            if px[j] < x1 or px[j] > x2:
                continue
            if py[j] < y1 or py[j] > y2:
                continue
            lcs = sqrt((px[j] - xx) ** 2 + (py[j] - yy) ** 2)
            if lcs < step:
                eop[j] = 0

    p = np
    for i in range(np+1, newnp):
        if eop[i] == 0:
            continue
        p = p + 1
        if i == p:
            continue
        bgeop[p] = bgeop[i]
        pstep[p] = pstep[i]
        eop[p] = eop[i]
        px[p] = px[i]
        py[p] = py[i]
    newnp = p
    nsearch = 0
    for i in range(0, ne):
        epoch[i] = 0


# ***************************************
def background_grid():
    # include 't0.inc'
    pmax = 100000
    emax = 200000
    delmax = 1000
    bmax = 2000
    fmin = 10 ** -8
    fm2 = 10 ** -8

    # global np, ne, nsearch, px, py, cx, cy, cr, nod, noe, epoch, ipx, ipy, centx, centy, length
    # px = np.empty(pmax, float)
    # py = np.empty(pmax, float)
    # ipx = np.empty(4, float)
    # ipy = np.empty(4, float)
    # centx = 0.0
    # centy = 0.0
    # length = 0.0
    # nod = np.empty((3, emax), int)
    # noe = np.empty((3, emax), int)
    # epoch = np.empty(emax, int)
    # cx = np.empty(emax, float)
    # cy = np.empty(pmax, float)
    # cr = np.empty(pmax, float)
    #
    # global gx, gy, gcx, gcy, gcr, x, y, xce, yce
    # gx = np.empty(3, float)
    # gy = np.empty(3, float)
    # gcx = 0.0
    # gcy = 0.0
    # gcr = 0.0
    # x = 0.0
    # y = 0.0
    # xce = 0.0
    # yce = 0.0
    #
    # global ndel, edel, neibn
    # ndel = 0
    # edel = np.empty(delmax, int)
    # neibn = np.empty(delmax, int)
    #
    # global eos, side, nb, nps
    # eos = np.empty((2, bmax), int)
    # side = np.empty((3, bmax), int)
    # nb = 0
    # nps = 0
    #
    # global newnp, ecrit, eop, bgeop, pstep
    # newnp = 0
    # ecrit = np.empty(emax, int)
    # eop = np.empty(pmax, int)
    # bgeop = np.empty(pmax, int)
    # pstep = np.empty(pmax, float)
    #
    # global bgnp, bgne, bgstep, bgfail, bgsearch, bgepoch
    # global bgpx, bgpy, bgcx, bgcy, bgcr, bgnod, bgnoe
    # bgnp = 0
    # bgne = 0
    # bgfail = 0
    # bgsearch = 0
    # bgpx = np.empty(pmax, float)
    # bgpy = np.empty(pmax, float)
    # bgstep = np.empty(pmax, float)
    # bgnod = np.empty((3, emax), int)
    # bgnoe = np.empty((3, emax), int)
    # bgepoch = np.empty(emax, int)
    # bgcx = np.empty(emax, float)
    # bgcy = np.empty(emax, float)
    # bgcr = np.empty(emax, float)

    i = 0
    j = 0
    # bgn = open("bgnod.dat", "r+")
    # bgno = open("bgnoe", "r+")
    # bgg = open("bggridt.dat", "r+")
    # bgs = open("bgstep.dat", "r+")
    # bgne = bgn.read(1)
    # bgnp = bgg.read(1)
    # for i in range(0, bgnp):
    #     bgpx[i], bgpy[i] = bgg.read(2)
    #     bgstep[i] = bgs.read(1)
    # # bgstep(i)=0.085
    # for i in range(0, bgne):
    #     bgnod[0, i], bgnod[1, i], bgnod[2, i] = bgn.read(3)
    #     bgnoe[0, i], bgnoe[1, i], bgnoe[2, i] = bgno.read(3)
    # bgn.close()
    # bgno.close()
    # bgg.close()
    # bgs.close()
    for i in range(0, bgne):
        for j in range(0, 3):
            gx[j] = bgpx[bgnod[j, i]]
            gy[j] = bgpy[bgnod[j, i]]
        circumcircle()
        bgcx[i] = gcx
        bgcy[i] = gcy
        bgcr[i] = gcr
    background_grid()


# ****************************************************
def search_in_bg(xx, yy, start, result, step):
    # include 't0.inc'
    pmax = 100000
    emax = 200000
    delmax = 1000
    bmax = 2000
    fmin = 10 ** -8
    fm2 = 10 ** -8

    # global np, ne, nsearch, px, py, cx, cy, cr, nod, noe, epoch, ipx, ipy, centx, centy, length
    # px = np.empty(pmax, float)
    # py = np.empty(pmax, float)
    # ipx = np.empty(4, float)
    # ipy = np.empty(4, float)
    # centx = 0.0
    # centy = 0.0
    # length = 0.0
    # nod = np.empty((3, emax), int)
    # noe = np.empty((3, emax), int)
    # epoch = np.empty(emax, int)
    # cx = np.empty(emax, float)
    # cy = np.empty(pmax, float)
    # cr = np.empty(pmax, float)
    #
    # global gx, gy, gcx, gcy, gcr, x, y, xce, yce
    # gx = np.empty(3, float)
    # gy = np.empty(3, float)
    # gcx = 0.0
    # gcy = 0.0
    # gcr = 0.0
    # x = 0.0
    # y = 0.0
    # xce = 0.0
    # yce = 0.0
    #
    # global ndel, edel, neibn
    # ndel = 0
    # edel = np.empty(delmax, int)
    # neibn = np.empty(delmax, int)
    #
    # global eos, side, nb, nps
    # eos = np.empty((2, bmax), int)
    # side = np.empty((3, bmax), int)
    # nb = 0
    # nps = 0
    #
    # global newnp, ecrit, eop, bgeop, pstep
    # newnp = 0
    # ecrit = np.empty(emax, int)
    # eop = np.empty(pmax, int)
    # bgeop = np.empty(pmax, int)
    # pstep = np.empty(pmax, float)
    #
    # global bgnp, bgne, bgstep, bgfail, bgsearch, bgepoch
    # global bgpx, bgpy, bgcx, bgcy, bgcr, bgnod, bgnoe
    # bgnp = 0
    # bgne = 0
    # bgfail = 0
    # bgsearch = 0
    # bgpx = np.empty(pmax, float)
    # bgpy = np.empty(pmax, float)
    # bgstep = np.empty(pmax, float)
    # bgnod = np.empty((3, emax), int)
    # bgnoe = np.empty((3, emax), int)
    # bgepoch = np.empty(emax, int)
    # bgcx = np.empty(emax, float)
    # bgcy = np.empty(emax, float)
    # bgcr = np.empty(emax, float)

    xx = 0.0
    yy = 0.0
    step = 0.0
    start = 0
    result = 0
    i = 0
    j = 0
    nei = 0
    k = 0
    last = 0
    next = 0
    current = 0
    e = 0
    arr = np.empty([3, 3], float)
    dcp = 0.0
    dep = 0.0
    bulk = np.empty(3, float)
    v1 = 0.0
    v2 = 0.0
    v3 = 0.0
    v4 = 0.0
    bgsearch = bgsearch + 1
    current = start
    result = 0
    next = 0
    last = 0
    for i in range(0, bgne):
        if bgepoch[current] == bgsearch:
            break
        gcx = bgcx[current]
        gcy = bgcy[current]
        gcr = bgcr[current]
        dcp = sqrt((xx - gcx) ** 2 + (yy - gcy) ** 2)
        if (dcp - gcr) < gcr * fm2:
            result = current
            break
        bgepoch[current] = bgsearch
        dep = -1
        next = 0
        for j in range(0, 3):
            nei = bgnoe[j, current]
            if nei < 1 or nei == last or bgepoch[nei] == bgsearch:
                continue
            gcx = bgcx[nei]
            gcy = bgcy[nei]
            gcr = bgcr[nei]
            dcp = sqrt((xx - gcx) ** 2 + (yy - gcy) ** 2)
            if (dcp - gcr) < gcr * fm2:
                result = current
                break
            xce = 0
            yce = 0
            for k in range(0, 3):
                xce = xce + bgpx[bgnod[k, nei]] / 3.0
                yce = yce + bgpy[bgnod[k, nei]] / 3.0
            dcp = sqrt((xx - xce) ** 2 + (yy - yce) ** 2)
            if dep < 0 or dep > dcp:
                dep = dcp
                next = nei
        if next == 0:
            break
        last = current
        current = next
    current = result
    result = 0
    if current > 0:
        for i in range(0, 3):
            for j in range(0, 3):
                arr[0, j] = 1
                arr[1, j] = bgpx[bgnod[j, current]]
                arr[2, j] = bgpy[bgnod[j, current]]
            arr[1, i] = xx
            arr[2, i] = yy
            det(arr, 3, bulk[i])
        v1 = bulk[0] + bulk[1] + bulk[2]
        v2 = abs(bulk[0]) + abs(bulk[1]) + abs(bulk[2])
        v3 = (v2 - v1) / v1
        if v3 < 10 ** -8:
            result = current
            step = 0
            for i in range(0, 3):
                bulk[i] = bulk[i] / v1
                step = step + bgstep[bgnod[i, result]] * bulk[i]
        else:
            search_bg_all(xx, yy, current)
            for i in range(0, ndel):
                e = edel[i]
                for k in range(0, 3):
                    for j in range(0, 3):
                        arr[0, j] = 1
                        arr[1, j] = bgpx[bgnod[j, e]]
                        arr[2, j] = bgpy[bgnod[j, e]]
                    arr[1, k] = xx
                    arr[2, k] = yy
                    det(arr, 3, bulk[k])
                v1 = bulk[0] + bulk[1] + bulk[2]
                v2 = abs(bulk[0]) + abs(bulk[1]) + abs(bulk[2])
                v4 = (v2 - v1) / v1
                if v4 < 10 ** -8:
                    result = e
                    step = 0
                    for k in range(0, 3):
                        bulk[k] = bulk[k] / v1
                        step = step + bgstep[bgnod[k, result]] * bulk[k]
                    break

    if result == 0:
        for i in range(bgne, 0, -1):
            gcx = bgcx[i]
            gcy = bgcy[i]
            gcr = bgcr[i]
            dcp = sqrt((xx - gcx) ** 2 + (yy - gcy) ** 2)
            if (dcp - gcr) < gcr * fm2:
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
                if v4 < 10 ** -8:
                    result = i
                    step = 0
                    for k in range(0, 3):
                        bulk[k] = bulk[k] / v1
                        step = step + bgstep[bgnod[k, result]] * bulk[k]
                    break


# ******************************************************
def search_boun(xx, yy, result, step):
    # include 't0.inc'
    pmax = 100000
    emax = 200000
    delmax = 1000
    bmax = 2000
    fmin = 10 ** -8
    fm2 = 10 ** -8

    # global np, ne, nsearch, px, py, cx, cy, cr, nod, noe, epoch, ipx, ipy, centx, centy, length
    # px = np.empty(pmax, float)
    # py = np.empty(pmax, float)
    # ipx = np.empty(4, float)
    # ipy = np.empty(4, float)
    # centx = 0.0
    # centy = 0.0
    # length = 0.0
    # nod = np.empty((3, emax), int)
    # noe = np.empty((3, emax), int)
    # epoch = np.empty(emax, int)
    # cx = np.empty(emax, float)
    # cy = np.empty(pmax, float)
    # cr = np.empty(pmax, float)
    #
    # global gx, gy, gcx, gcy, gcr, x, y, xce, yce
    # gx = np.empty(3, float)
    # gy = np.empty(3, float)
    # gcx = 0.0
    # gcy = 0.0
    # gcr = 0.0
    # x = 0.0
    # y = 0.0
    # xce = 0.0
    # yce = 0.0
    #
    # global ndel, edel, neibn
    # ndel = 0
    # edel = np.empty(delmax, int)
    # neibn = np.empty(delmax, int)
    #
    # global eos, side, nb, nps
    # eos = np.empty((2, bmax), int)
    # side = np.empty((3, bmax), int)
    # nb = 0
    # nps = 0
    #
    # global newnp, ecrit, eop, bgeop, pstep
    # newnp = 0
    # ecrit = np.empty(emax, int)
    # eop = np.empty(pmax, int)
    # bgeop = np.empty(pmax, int)
    # pstep = np.empty(pmax, float)
    #
    # global bgnp, bgne, bgstep, bgfail, bgsearch, bgepoch
    # global bgpx, bgpy, bgcx, bgcy, bgcr, bgnod, bgnoe
    # bgnp = 0
    # bgne = 0
    # bgfail = 0
    # bgsearch = 0
    # bgpx = np.empty(pmax, float)
    # bgpy = np.empty(pmax, float)
    # bgstep = np.empty(pmax, float)
    # bgnod = np.empty((3, emax), int)
    # bgnoe = np.empty((3, emax), int)
    # bgepoch = np.empty(emax, int)
    # bgcx = np.empty(emax, float)
    # bgcy = np.empty(emax, float)
    # bgcr = np.empty(emax, float)

    xx = 0.0
    yy = 0.0
    step = 0.0
    i = 0
    j = 0
    k = 0
    nbg = np.empty(3, int)
    arr = np.empty([3, 3], float)
    dcp = 0
    bulk = np.empty(3, float)
    v1 = 0
    v2 = 0
    v4 = 0
    vol = np.empty(3, float)
    vmin = 1.0
    emin = 0
    result = 0
    for i in range(bgne, 0, -1):
        nbg[0] = bgnoe[0, i]
        nbg[1] = bgnoe[1, i]
        nbg[2] = bgnoe[2, i]
        if nbg[0] != 0 and nbg[1] != 0 and nbg[2] != 0:
            continue
        gcx = bgcx[i]
        gcy = bgcy[i]
        gcr = bgcr[i]
        dcp = sqrt((xx - gcx) ** 2 + (yy - gcy) ** 2)
        #  if((dcp-gcr)<gcr*fm2*1000)then
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
        # if(v4<1e-4)then
        if vmin > v4:
            vmin = v4
            emin = i
            vol[0] = bulk[0]
            vol[1] = bulk[1]
            vol[2] = bulk[2]
    if emin == 0:
        return
    v1 = vol[0] + vol[1] + vol[2]
    v2 = abs(vol[0]) + abs(vol[1]) + abs(vol[2])
    v4 = v1 + v2
    step = 0
    for k in range(0, 3):
        vol[k] = (vol[k] + abs(vol[k])) / v4
        step = step + bgstep[bgnod[k, emin]] * vol[k]
    result = emin


# **********************************************
def search_bg_all(xx, yy, ending):
    # include 't0.inc'
    pmax = 100000
    emax = 200000
    delmax = 1000
    bmax = 2000
    fmin = 10 ** -8
    fm2 = 10 ** -8

    # global np, ne, nsearch, px, py, cx, cy, cr, nod, noe, epoch, ipx, ipy, centx, centy, length
    # px = np.empty(pmax, float)
    # py = np.empty(pmax, float)
    # ipx = np.empty(4, float)
    # ipy = np.empty(4, float)
    # centx = 0.0
    # centy = 0.0
    # length = 0.0
    # nod = np.empty((3, emax), int)
    # noe = np.empty((3, emax), int)
    # epoch = np.empty(emax, int)
    # cx = np.empty(emax, float)
    # cy = np.empty(pmax, float)
    # cr = np.empty(pmax, float)
    #
    # global gx, gy, gcx, gcy, gcr, x, y, xce, yce
    # gx = np.empty(3, float)
    # gy = np.empty(3, float)
    # gcx = 0.0
    # gcy = 0.0
    # gcr = 0.0
    # x = 0.0
    # y = 0.0
    # xce = 0.0
    # yce = 0.0
    #
    # global ndel, edel, neibn
    # ndel = 0
    # edel = np.empty(delmax, int)
    # neibn = np.empty(delmax, int)
    #
    # global eos, side, nb, nps
    # eos = np.empty((2, bmax), int)
    # side = np.empty((3, bmax), int)
    # nb = 0
    # nps = 0
    #
    # global newnp, ecrit, eop, bgeop, pstep
    # newnp = 0
    # ecrit = np.empty(emax, int)
    # eop = np.empty(pmax, int)
    # bgeop = np.empty(pmax, int)
    # pstep = np.empty(pmax, float)
    #
    # global bgnp, bgne, bgstep, bgfail, bgsearch, bgepoch
    # global bgpx, bgpy, bgcx, bgcy, bgcr, bgnod, bgnoe
    # bgnp = 0
    # bgne = 0
    # bgfail = 0
    # bgsearch = 0
    # bgpx = np.empty(pmax, float)
    # bgpy = np.empty(pmax, float)
    # bgstep = np.empty(pmax, float)
    # bgnod = np.empty((3, emax), int)
    # bgnoe = np.empty((3, emax), int)
    # bgepoch = np.empty(emax, int)
    # bgcx = np.empty(emax, float)
    # bgcy = np.empty(emax, float)
    # bgcr = np.empty(emax, float)

    ending = 0
    ele = 0
    nei = 0
    # num = 0
    k = 0
    xx = 0.0
    yy = 0.0
    dcp = 0.0
    ndel = 1
    edel[ndel] = ending
    num = 1
    bgepoch[ending] = -bgsearch
    while True:
        ele = edel[num]
        for k in range(0, 3):
            nei = bgnoe[k, ele]
            if nei <= 0 or bgepoch[nei] == -bgsearch:
                continue
            gcx = bgcx[nei]
            gcy = bgcy[nei]
            gcr = bgcr[nei]
            dcp = sqrt((xx - gcx) ** 2 + (yy - gcy) ** 2)
            if (dcp - gcr) < (fm2 * gcr):
                ndel = ndel + 1
                edel[ndel] = nei
                bgepoch[nei] = -bgsearch
        num = num + 1
        if num > ndel:
            break


# ************************************************************************
def smooth():
    # include 't0.inc'
    pmax = 100000
    emax = 200000
    delmax = 1000
    bmax = 2000
    fmin = 10 ** -8
    fm2 = 10 ** -8

    # global np, ne, nsearch, px, py, cx, cy, cr, nod, noe, epoch, ipx, ipy, centx, centy, length
    np=0
    # px = np.empty(pmax, float)
    # py = np.empty(pmax, float)
    # ipx = np.empty(4, float)
    # ipy = np.empty(4, float)
    # centx = 0.0
    # centy = 0.0
    # length = 0.0
    # nod = np.empty((3, emax), int)
    # noe = np.empty((3, emax), int)
    # epoch = np.empty(emax, int)
    # cx = np.empty(emax, float)
    # cy = np.empty(pmax, float)
    # cr = np.empty(pmax, float)
    #
    # global gx, gy, gcx, gcy, gcr, x, y, xce, yce
    # gx = np.empty(3, float)
    # gy = np.empty(3, float)
    # gcx = 0.0
    # gcy = 0.0
    # gcr = 0.0
    # x = 0.0
    # y = 0.0
    # xce = 0.0
    # yce = 0.0
    #
    # global ndel, edel, neibn
    # ndel = 0
    # edel = np.empty(delmax, int)
    # neibn = np.empty(delmax, int)
    #
    # global eos, side, nb, nps
    # eos = np.empty((2, bmax), int)
    # side = np.empty((3, bmax), int)
    # nb = 0
    # nps = 0
    #
    # global newnp, ecrit, eop, bgeop, pstep
    # newnp = 0
    # ecrit = np.empty(emax, int)
    # eop = np.empty(pmax, int)
    # bgeop = np.empty(pmax, int)
    # pstep = np.empty(pmax, float)
    #
    # global bgnp, bgne, bgstep, bgfail, bgsearch, bgepoch
    # global bgpx, bgpy, bgcx, bgcy, bgcr, bgnod, bgnoe
    # bgnp = 0
    # bgne = 0
    # bgfail = 0
    # bgsearch = 0
    # bgpx = np.empty(pmax, float)
    # bgpy = np.empty(pmax, float)
    # bgstep = np.empty(pmax, float)
    # bgnod = np.empty((3, emax), int)
    # bgnoe = np.empty((3, emax), int)
    # bgepoch = np.empty(emax, int)
    # bgcx = np.empty(emax, float)
    # bgcy = np.empty(emax, float)
    # bgcr = np.empty(emax, float)

    m = 0
    n = 0
    i = 0
    j = 0
    k = 0
    p = 0
    nei = 0
    bgep = 0
    ep = 0
    pp = npp.empty(3, int)
    p2 = npp.empty(3, int)
    s1 = npp.empty(3, float)
    slmin = 0.0
    stmin = 0.0
    xx = 0.0
    yy = 0.0
    step = 0.0
    lcs = 0.0
    x1 = 0.0
    x2 = 0.0
    y1 = 0.0
    y2 = 0.0
    vx = 0.0
    vy = 0.0
    f1 = 0.5
    f2 = 1.2
    f5 = 1.0
    f3 = 0.3
    f4 = 0.5
    newnp = np
    bgsearch = 0
    for i in range(0, bgne):
        bgepoch[i] = 0
    for i in range(0, ne):
        pp[0] = nod[0, i]
        pp[1] = nod[1, i]
        pp[2] = nod[2, i]
        for j in range(0, 3):
            m = j + 1
            n = j + 2
            if m > 3:
                m = m - 3
            if n > 3:
                n = n - 3
            sl[j] = sqrt((px[pp[m]] - px[pp[n]]) ** 2 + (py[pp[m]] - py[pp[n]]) ** 2)
        slmin = min(sl[0], sl[1], sl[2])
        stmin = min(pstep[pp[0]], pstep[pp[1]], pstep[pp[2]])
        if cr[i] > slmin * f2 or cr[i] > stmin * f5:
            xx = cx[i]
            yy = cy[i]
            search_in_bg(xx, yy, bgeop[pp[0]], bgep, step)
            if bgep == 0:
                continue
            p = newnp + 1
            px[p] = xx
            py[p] = yy
            j = min(i, ne)
            search_1st(p, j, ep)
            if ep == 0:
                continue
            p2[0] = nod[0, ep]
            p2[1] = nod[1, ep]
            p2[2] = nod[2, ep]
            for k in range(0, 3):
                nei = noe[k, ep]
                if nei != 0:
                    continue
                m = k + 1
                n = m + 1
                if m > 3:
                    m = m - 3
                if n > 3:
                    n = n - 3
                vx = py[p2[m]] - py[p2[n]]
                vy = px[p2[n]] - px[p2[m]]
                lcs = sqrt(vx * vx + vy * vy)
                vx = vx / lcs
                vy = vy / lcs
                lcs = abs(vx * (xx - px[p2[n]]) + vy * (yy - py[p2[n]]))
                if lcs < f3 * step:
                    p = 0
                    break
            if p == 0:
                continue
            search_all(p, ep)
            for j in range(0, ndel):
                for k in range(0, 3):
                    vx = px[nod[k, edel[j]]]
                    vy = py[nod[k, edel[j]]]
                    lcs = sqrt((vx - xx) ** 2 + (vy - yy) ** 2)
                    if (lcs < f4 * step) and (lcs < slmin * f4):
                        p = 0
                        break
                if p == 0:
                    break
            if p=0:
                continue
            newnp = newnp + 1
            px[newnp] = xx
            py[newnp] = yy
            bgeop[newnp] = bgep
            pstep[newnp] = step
            eop[newnp] = ep
    for i in range(np+1, newnp):
        if eop[i] == 0:
            continue
        for j in range(i + 1, newnp):
            if eop[j] == 0:
                continue
            if pstep[j] < pstep[i]:
                xx = px[i]
                px[i] = px[j]
                px[j] = xx
                yy = py[i]
                py[i] = py[j]
                py[j] = yy
                step = pstep[i]
                pstep[i] = pstep[j]
                pstep[j] = step
                ep = eop[i]
                eop[i] = eop[j]
                eop[j] = ep
                bgep = bgeop[i]
                bgeop[i] = bgeop[j]
                bgeop[j] = bgep
        xx = px[i]
        yy = py[i]
        step = pstep[i] * f1
        x1 = xx - step
        x2 = xx + step
        y1 = yy - step
        y2 = yy + step
        for j in range(i + 1, newnp):
            if px[j] < x1 or px[j] > x2:
                continue
            if py[j] < y1 or py[j] > y2:
                continue
            lcs = sqrt((px[j] - xx) ** 2 + (py[j] - yy) ** 2)
            if lcs < step:
                eop[j] = 0
    p = np
    for i in range(np + 1, newnp):
        if eop[i] == 0:
            continue
        p = p + 1
        if i == p:
            continue
        bgeop[p] = bgeop[i]
        pstep[p] = pstep[i]
        eop[p] = eop[i]
        px[p] = px[i]
        py[p] = py[i]
    newnp = p
    for i in range(np + 1, newnp):
        k = eop[i]
        if k > ne:
            k = ne
        search_1st(i, k, j)
        if j == 0:
            print("error:search_ist=0/i=", i)
            j = input()
            break
        search_all(i, j)
        if ndel > 200:
            print("ndel=", ndel, "/i=", i)
            k = input()
        check_up(i)
        clear_up(i)
        if i % 1000 == 0:
            print("i=", i, ne)
    np = newnp
    print("smooth over,  np=", np, ',  ne=', ne)


def optimize():
    # include 't0.inc'
    pmax = 100000
    emax = 200000
    delmax = 1000
    bmax = 2000
    fmin = 10 ** -8
    fm2 = 10 ** -8

    # global np, ne, nsearch, px, py, cx, cy, cr, nod, noe, epoch, ipx, ipy, centx, centy, length
    # px = np.empty(pmax, float)
    # py = np.empty(pmax, float)
    # ipx = np.empty(4, float)
    # ipy = np.empty(4, float)
    # centx = 0.0
    # centy = 0.0
    # length = 0.0
    # nod = np.empty((3, emax), int)
    # noe = np.empty((3, emax), int)
    # epoch = np.empty(emax, int)
    # cx = np.empty(emax, float)
    # cy = np.empty(pmax, float)
    # cr = np.empty(pmax, float)
    #
    # global gx, gy, gcx, gcy, gcr, x, y, xce, yce
    # gx = np.empty(3, float)
    # gy = np.empty(3, float)
    # gcx = 0.0
    # gcy = 0.0
    # gcr = 0.0
    # x = 0.0
    # y = 0.0
    # xce = 0.0
    # yce = 0.0
    #
    # global ndel, edel, neibn
    # ndel = 0
    # edel = np.empty(delmax, int)
    # neibn = np.empty(delmax, int)
    #
    # global eos, side, nb, nps
    # eos = np.empty((2, bmax), int)
    # side = np.empty((3, bmax), int)
    # nb = 0
    # nps = 0
    #
    # global newnp, ecrit, eop, bgeop, pstep
    # newnp = 0
    # ecrit = np.empty(emax, int)
    # eop = np.empty(pmax, int)
    # bgeop = np.empty(pmax, int)
    # pstep = np.empty(pmax, float)
    #
    # global bgnp, bgne, bgstep, bgfail, bgsearch, bgepoch
    # global bgpx, bgpy, bgcx, bgcy, bgcr, bgnod, bgnoe
    # bgnp = 0
    # bgne = 0
    # bgfail = 0
    # bgsearch = 0
    # bgpx = np.empty(pmax, float)
    # bgpy = np.empty(pmax, float)
    # bgstep = np.empty(pmax, float)
    # bgnod = np.empty((3, emax), int)
    # bgnoe = np.empty((3, emax), int)
    # bgepoch = np.empty(emax, int)
    # bgcx = np.empty(emax, float)
    # bgcy = np.empty(emax, float)
    # bgcr = np.empty(emax, float)

    newx = np.empty(pmax, float)
    newy = np.empty(pmax, float)
    i = 0
    times = 0
    newn = np.empty(pmax, float)
    p1 = 0
    p2 = 0
    p3 = 0
    print("optimizing start!")
    for times in range(0, 100):
        for i in range(0, np):
            newx[i] = 0
            newy[i] = 0
            newn[i] = 0
        for i in range(0, ne):
            p1 = nod[0, i]
            p2 = nod[1, i]
            p3 = nod[2, i]
            x = px[p1] + px[p2] + px[p3]
            y = py[p1] + py[p2] + py[p3]
            newn[p1] = newn[p1] + 3
            newx[p1] = newx[p1] + x
            newy[p1] = newy[p1] + y
            newn[p2] = newn[p2] + 3
            newx[p2] = newx[p2] + x
            newy[p2] = newy[p2] + y
            newn[p3] = newn[p3] + 3
            newx[p3] = newx[p3] + x
            newy[p3] = newy[p3] + y
        for i in range(nps + 1, np):
            px[i] = newx[i] / newn[i]
            py[i] = newy[i] / newn[i]
