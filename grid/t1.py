import numpy as np
pmax=100000
emax=200000
bmax=50000
fmin=10**-8
fm2=10**-8

gx=np.empty(3, float)
gy=np.empty(3, float)
global gx, gy, gcx, gcy, gcr, x, y, xce, yce


px=np.empty(pmax, float)
py=np.empty(pmax, float)
step=np.empty(pmax, float)
nod=np.empty([3, emax], int)
noe=np.empty([3, emax], int)
cx=np.empty(emax, float)
cy=np.empty(emax, float)
cr=np.empty(emax, float)
volu=np.empty([3, emax], float)
global np, ne, step
global px, py, cx, cy, cr, nod, noe, volu

