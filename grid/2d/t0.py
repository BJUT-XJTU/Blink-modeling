import numpy as npp
from math import sqrt

# global pmax, emax, delmax, bmax
# global fmin, fm2
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




