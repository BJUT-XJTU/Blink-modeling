pmax=100000
emax=200000

global nod, px, py, npx, npy, bgeop, ne, nnp, np, u, v, p, r, unew, vnew, pnew, rnew
nod=np.empty((3, emax), int)
bgeop=np.empty(pmax, int)
nnp=0
np=0
ne=0
px=np.empty(pmax, float)
py=np.empty(pmax, float)
npx=np.empty(pmax, float)
npy=np.empty(pmax, float)
u=np.empty(pmax, float)
v=np.empty(pmax, float)
p=np.empty(pmax, float)
r=np.empty(pmax, float)
unew=np.empty(pmax, float)
vnew=np.empty(pmax, float)
pnew=np.empty(pmax, float)
rnew=np.empty(pmax, float)