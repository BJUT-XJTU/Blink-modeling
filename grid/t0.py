import numpy as np
B_WALL=1
B_INFLOW=2
B_OUTFLOW=4
B_SYMMETRY=8
B_SOURCE=16
PMAX=50000
EMAX=100000
NVEX = 3
MAX_NITERATION = 1000
UNITEC=1.610217733
MOLNUM=6.0221367

NPOCH=np.empty(PMAX, int)
NOD=np.empty([NVEX, EMAX], int)
NOE=np.empty([NVEX, EMAX], int)
PX=np.empty(PMAX, float)
PY=np.empty(PMAX, float)
CTRL_AREA=np.empty(PMAX, float)
global NP, NE, NPOCH, NOD, NOE, PX, PY
global CTRL_AREA, TOTAL_AREA


EFVM=np.empty([3, EMAX], float)
PFVM=np.empty(PMAX, float)
BFVM=np.empty(PMAX, float)
AFVM=np.empty(PMAX, float)
CFVM=np.empty(PMAX, float)
global EFVM, PFVM, BFVM, AFVM, CFVM


CCAJSR=np.empty(PMAX, float)
NEWCCA=np.empty(PMAX, float)
MEDCCA=np.empty(PMAX, float)
RITER=np.empty(PMAX, float)
PITER=np.empty(PMAX, float)
APK=np.empty(PMAX, float)
global CCAJSR, NEWCCA, MEDCCA, RITER, PITER, APK
global DT, NSTEP, ILOAD, DSAVE, RELEASE_TIMES

global KDCSQ, DCAJSR, BCSQ, H_JSR
global CCAMYO, DCARYR
global CCAFSR, DCAFSR
global ICARYR, ICAFSR, AVG_CA_JSR




