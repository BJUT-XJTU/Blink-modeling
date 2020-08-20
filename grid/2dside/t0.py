import numpy as npp
from math import sqrt

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

