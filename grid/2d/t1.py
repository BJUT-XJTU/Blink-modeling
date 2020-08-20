pmax=50000
emax=100000

global px, py, np, ne, nod, pstep, be, ce, vol, alv, ex, ey, p, r, u, v, dr, norm
px=np.empty(pmax, float)
py=np.empty(pmax, float)
alv=np.empty(pmax, float)
pstep=np.empty(pmax, float)
be=np.empty((3, emax), float)
ce=np.empty((3, emax), float)
vol=np.empty(emax, float)
u=np.empty(pmax, float)
v=np.empty(pmax, float)
p=np.empty(pmax, float)
r=np.empty(pmax, float)
dr=np.empty(pmax, float)
ex=np.empty(emax, float)
ey=np.empty(emax, float)
norm=0.0
nod=np.empty((3, emax), int)
np=0
ne=0
