import numpy as np
from math import sqrt

global B_WALL, B_INFLOW, B_OUTFLOW, B_SYMMETRY, B_SOURCE, PMAX, EMAX, NVEX, MAX_NITERATION, UNITEC, MOLNUM
global NP, NE, NPOCH, NOD, NOE, PX, PY
global CTRL_AREA, TOTAL_AREA
global EFVM, PFVM, BFVM, AFVM, CFVM
global CCAJSR, NEWCCA, MEDCCA, RITER, PITER, APK
global DT, NSTEP, ILOAD, RELEASE_TIMES
global DSAVE
global KDCSQ, DCAJSR, BCSQ, H_JSR
global CCAMYO, DCARYR
global CCAFSR, DCAFSR
global ICARYR, ICAFSR, AVG_CA_JSR

ICARYR = 0.0
ICAFSR = 0.0
AVG_CA_JSR = 0.0

CCAFSR = 0.0
CCAMYO = 0.0
KDCSQ = 0.0
DCAJSR = 0.0
BCSQ = 0.0
DCARYR = 0.0
DCAFSR = 0.0
H_JSR = 0.0

DT = 0.0
NSTEP = 0.0
ILOAD = 0.0
RELEASE_TIMES = 0.0
DSAVE = 0

B_WALL = 1  # 基质网原始Ca离子浓度
B_INFLOW = 2  # Ca离子进入口
B_OUTFLOW = 4  # Ca离子输出口
B_SYMMETRY = 8
B_SOURCE = 16
PMAX = 50000  # # 点数
EMAX = 100000  # 三角形单元数
NVEX = 3  # 三角形顶点数
MAX_NITERATION = 1000
UNITEC = 1.610217733  # 一个电荷的常数
MOLNUM = 6.0221367  # 摩尔常熟，单位

NP = 0  # 节点个数
NE = 0  # NE为三角形单元的数量
NPOCH = np.empty(PMAX, int)  # 每个节点的属性
NOD = np.empty([NVEX, EMAX], int)  # 这些节点组成的三角形单元的信息
NOE = np.empty([NVEX, EMAX], int)  # 这个是每一个三角形单元的三个邻居单元的编号
PX = np.empty(PMAX, float)  # 点的横坐标
PY = np.empty(PMAX, float)  # 点的纵坐标
CTRL_AREA = np.empty(PMAX, float)  # 每一个点对应的三角形单元面积
TOTAL_AREA = 0.0  # TOTAL_AREA区域的面积

EFVM = np.empty([3, EMAX], float)  # 每个三角形单元对应的系数
PFVM = np.empty(PMAX, float)  # 系数
BFVM = np.empty(PMAX, float)  # 系数
AFVM = np.empty(PMAX, float)  # 系数
CFVM = np.empty(PMAX, float)  # 系数，对应的scan.pdf中的a，b，c，d

CCAJSR = np.empty(PMAX, float)  # 肌质网每一点钙的浓度
NEWCCA = np.empty(PMAX, float)
MEDCCA = np.empty(PMAX, float)  # 临时变量
RITER = np.empty(PMAX, float)  # 临时
PITER = np.empty(PMAX, float)  # 临时
APK = np.empty(PMAX, float)  # 临时


def AVERAGE_CCA():
    global NP
    global B_WALL, B_INFLOW, B_OUTFLOW, B_SYMMETRY, B_SOURCE, PMAX, EMAX, NVEX, MAX_NITERATION, UNITEC, MOLNUM
    global NP, NE, NPOCH, NOD, NOE, PX, PY
    global CTRL_AREA, TOTAL_AREA
    global EFVM, PFVM, BFVM, AFVM, CFVM
    global CCAJSR, NEWCCA, MEDCCA, RITER, PITER, APK
    global DT, NSTEP, ILOAD, RELEASE_TIMES
    global DSAVE
    global KDCSQ, DCAJSR, BCSQ, H_JSR
    global CCAMYO, DCARYR
    global CCAFSR, DCAFSR
    global ICARYR, ICAFSR, AVG_CA_JSR

    # INCLUDE 'T0.INC'

    I = 0
    TOTAL_CA = 0.0
    for I in range(0, NP + 1):
        TOTAL_CA = TOTAL_CA + CCAJSR[I] * CTRL_AREA[I]  # 每一点Ca的浓度X每一个点对应的三角形单元面积=每一点钙的总面积
    if TOTAL_AREA > 0.00000000000001:
        AVG_CA_JSR = TOTAL_CA / TOTAL_AREA  # JSR平均浓度


# ***************************************
def CA_CURRENT():
    global NP
    global B_WALL, B_INFLOW, B_OUTFLOW, B_SYMMETRY, B_SOURCE, PMAX, EMAX, NVEX, MAX_NITERATION, UNITEC, MOLNUM
    global NP, NE, NPOCH, NOD, NOE, PX, PY
    global CTRL_AREA, TOTAL_AREA
    global EFVM, PFVM, BFVM, AFVM, CFVM
    global CCAJSR, NEWCCA, MEDCCA, RITER, PITER, APK
    global DT, NSTEP, ILOAD, RELEASE_TIMES
    global DSAVE
    global KDCSQ, DCAJSR, BCSQ, H_JSR
    global CCAMYO, DCARYR
    global CCAFSR, DCAFSR
    global ICARYR, ICAFSR, AVG_CA_JSR
    I = 0
    N1 = 0
    N2 = 0
    N3 = 0
    CA_IN = 0.0
    CA_OUT = 0.0
    LENGTH = 0.0
    for I in range(0, NE):
        N1 = NOD[0, I]
        N2 = NOD[1, I]
        N3 = NOD[2, I]
        #  OUT CURRENT
        if (NPOCH[N1] == B_OUTFLOW) and (NPOCH[N2] == B_OUTFLOW):
            LENGTH = sqrt((PX[N1] - PX[N2]) ** 2 + (PY[N1] - PY[N2]) ** 2)
            CA_OUT = CA_OUT + LENGTH * (CCAJSR[N1] + CCAJSR[N2]) / 2
        if (NPOCH[N3] == B_OUTFLOW) and (NPOCH[N2] == B_OUTFLOW):
            LENGTH = sqrt((PX[N3] - PX[N2]) ** 2 + (PY[N3] - PY[N2]) ** 2)
            CA_OUT = CA_OUT + LENGTH * (CCAJSR[N3] + CCAJSR[N2]) / 2
        if (NPOCH[N1] == B_OUTFLOW) and (NPOCH[N3] == B_OUTFLOW):
            LENGTH = sqrt((PX[N1] - PX[N3]) ** 2 + (PY[N1] - PY[N3]) ** 2)
            CA_OUT = CA_OUT + LENGTH * (CCAJSR[N1] + CCAJSR[N3]) / 2
        #  IN CURRENT
        if NPOCH[N1] == B_INFLOW and NPOCH[N2] == B_INFLOW:
            LENGTH = sqrt((PX[N1] - PX[N2]) ** 2 + (PY[N1] - PY[N2]) ** 2)
            CA_IN = CA_IN + LENGTH * (CCAFSR - (CCAJSR[N1] + CCAJSR[N2]) / 2)
        if NPOCH[N3] == B_INFLOW and NPOCH[N2] == B_INFLOW:
            LENGTH = sqrt((PX[N3] - PX[N2]) ** 2 + (PY[N3] - PY[N2]) ** 2)
            CA_IN = CA_IN + LENGTH * (CCAFSR - (CCAJSR[N3] + CCAJSR[N2]) / 2)
        if NPOCH[N1] == B_INFLOW and NPOCH[N3] == B_INFLOW:
            LENGTH = sqrt((PX[N1] - PX[N3]) ** 2 + (PY[N1] - PY[N3]) ** 2)
            CA_IN = CA_IN + LENGTH * (CCAFSR - (CCAJSR[N1] + CCAJSR[N3]) / 2)

    CA_OUT = CA_OUT * DCARYR * H_JSR
    CA_IN = CA_IN * DCAFSR * H_JSR
    ICARYR = CA_OUT * UNITEC * 2 * MOLNUM * (10.0 ** -11)
    ICAFSR = CA_IN * UNITEC * 2 * MOLNUM * (10.0 ** -11)


def not_empty(s):
    return s and s.strip()


def main():
    print("开始执行main()函数")
    LOAD_GRIDINFO()  # 网格的信息
    print("执行LOAD_GRIDINFO()函数")
    INITIAL_PARAMETER()  # 初始化参数
    print("执行INITIAL_PARAMETER()函数")
    COEFFICIENT()  # 调用的系数，离散化的系数
    print("执行COEFFICIENT()函数")
    DOLOOP_DIFFUSION()  # 循环，一步一步往前推
    print("执行DOLOOP_DIFFUSION()函数")


# *************************
def INITIAL_PARAMETER():
    # print("开始初始化参数")
    global NP
    global B_WALL, B_INFLOW, B_OUTFLOW, B_SYMMETRY, B_SOURCE, PMAX, EMAX, NVEX, MAX_NITERATION, UNITEC, MOLNUM
    global NP, NE, NPOCH, NOD, NOE, PX, PY
    global CTRL_AREA, TOTAL_AREA
    global EFVM, PFVM, BFVM, AFVM, CFVM
    global CCAJSR, NEWCCA, MEDCCA, RITER, PITER, APK
    global DT, NSTEP, ILOAD, RELEASE_TIMES
    global DSAVE
    global KDCSQ, DCAJSR, BCSQ, H_JSR
    global CCAMYO, DCARYR
    global CCAFSR, DCAFSR
    global ICARYR, ICAFSR, AVG_CA_JSR

    CCAFSR = 1.0  # 细管子
    CCAMYO = 0.0001  # 细胞的ca浓度
    BCSQ = 14.0  # ca和蛋白质结合的量
    KDCSQ = 0.63  # 方程中的K
    H_JSR = 30.0  # JSR的高度
    DCAJSR = 3.5 * 10 ** 8  # JSR的扩散系数
    DCARYR = 6.5 * 10 ** 7  # RYR的扩散系数
    DCAFSR = 0.7854 * 10 ** 6  # 扩散系数
    DT = 2 * 10 ** -6  # dt
    RELEASE_TIMES = 2 * 10 ** -2  # 0.02s,这个就是ryr通道开放的时间，后80毫秒是恢复的
    ILOAD = 1  # 第一次加载
    DSAVE = 100  # 每做100部保存一次
    NSTEP = 50000  # 程序执行的次数
    for I in range(0, NP + 1):  # 为肌质网每一点的初始钙浓度赋值为1
        CCAJSR[I] = 1.0


# *********************************
def DOLOOP_DIFFUSION():
    global NP
    global B_WALL, B_INFLOW, B_OUTFLOW, B_SYMMETRY, B_SOURCE, PMAX, EMAX, NVEX, MAX_NITERATION, UNITEC, MOLNUM
    global NP, NE, NPOCH, NOD, NOE, PX, PY
    global CTRL_AREA, TOTAL_AREA
    global EFVM, PFVM, BFVM, AFVM, CFVM
    global CCAJSR, NEWCCA, MEDCCA, RITER, PITER, APK
    global DT, NSTEP, ILOAD, RELEASE_TIMES
    global DSAVE
    global KDCSQ, DCAJSR, BCSQ, H_JSR
    global CCAMYO, DCARYR
    global CCAFSR, DCAFSR
    global ICARYR, ICAFSR, AVG_CA_JSR
    # print("开始进行基函数递归")
    global DCARYR
    global ILOAD
    I = 0
    J = 0
    # ?????????????
    # CURSTEP = 0
    # RELEASE_STEP = 0
    FILENAME = ""
    STRN = ""
    CURSTEP = 0
    save = open("DATA\\SAVE00000000.dat", "w")
    print("写入SAVE00000000中", NP)
    for I in range(0, NP + 1):
        save.write(str(CCAJSR[I]) + "\n")
    AVERAGE_CCA()  # 计算平均浓度 没问题
    CA_CURRENT()  # 计算0时刻电流 没问题
    # ?????
    save.write(str(AVG_CA_JSR) + "\n")  # NP
    save.write(str(ICARYR) + " ")  # NP + 1
    save.write(str(ICAFSR) + "\n")  # NP + 1
    save.write(str(CURSTEP) + "\n")  # NP + 2
    save.close()
    # print(AVG_CA_JSR,ICARYR,ICAFSR,CURSTEP)
    # -------------------------------------------------
    print("CURSTEP", CURSTEP)
    current_down = np.empty(130000, int)
    print("把数据写入SAVE00000000文件")
    if ILOAD == 1:  # 如果是第一次加载，就从save文件开始
        ILOAD = ILOAD + 1
        sav = open("SAVE.dat", "r")
        # 把哪里命名为SAVE文件，就从哪里打开，就从哪里继续运行程序
        # for I in range(0, NP):
        #     CCAJSR[I] = sav.read(1)
        # AVG_CA_JSR = sav.read(1)
        # ICARYR = sav.read(1)
        # ICAFSR = sav.read(1)
        # CURSTEP = sav.read(1)
        # sav.close()
        # ????????
        I = 0
        for line in sav.readlines():
            # print('I',I,NP+1,line)
            if I < NP + 1:
                # 把从save文件中读取到的0到NP位置的数据赋值给每一点Ca浓度所组成的数组CCAJSR，
                CCAJSR[I] = float(line)
            else:  # NP NP +1 NP + 2的文件数据读取
                if I == NP + 1:
                    # print("line", line, "NP", NP, "I", I)
                    AVG_CA_JSR = float(line)
                elif I == NP + 2:
                    tmp = line.split()
                    ICARYR = float(tmp[0])
                    ICAFSR = float(tmp[1])
                else:
                    CURSTEP = int(line)
            I = I + 1
        sav.close()

    # ----------------------------------------------------
    RELEASE_STEP = int((RELEASE_TIMES + (10 ** -6)) / DT)  # 释放时间的迭代次数

    # print("RELEASE_STEP", RELEASE_STEP, "RELEASE_TIMES", RELEASE_TIMES, "CURSTEP", CURSTEP)
    if CURSTEP >= RELEASE_STEP:
        DCARYR = 0
        COEFFICIENT()

    for J in range(CURSTEP + 1, NSTEP + 1):
        print("J", J, "CURSTEP", CURSTEP, "NSTEP", NSTEP)
        PREESTIMATE_EQUATION()  # 计算n+1/2 Ca的值 P11 1
        # -----------------------------------------------
        CORRECTION_EQUATION()  # 计算n+1步Ca的浓度 p12 2
        # -----------------------------------------------------
        for I in range(0, NP + 1):  # NP为点的个数
            CCAJSR[I] = NEWCCA[I]

        print('CCAJSR', CCAJSR)

        # ???????????????????????????????????
        # print("????????????")
        if (J) % DSAVE == 0:
            print("STEP =", J)
            STRN = str(J).zfill(8)
            print(STRN, "=", J)
            FILENAME = "DATA\\SAVE" + STRN + '.dat'
            FIL = open(FILENAME, "w")
            print("FILENAME", FILENAME)
            for I in range(0, NP + 1):
                FIL.write(str(CCAJSR[I]) + "\n")
            AVERAGE_CCA()
            CA_CURRENT()
            FIL.write(str(AVG_CA_JSR) + "\n")
            FIL.write(str(ICARYR) + " ")
            FIL.write(str(ICAFSR) + "\n")
            FIL.write(str(J + 1) + "\n")
            FIL.close()
        if J == RELEASE_STEP:
            DCARYR = 0
            COEFFICIENT()
    print("执行成功")


# *************************************************
def PREESTIMATE_EQUATION():  # 构建n+ 1/2步的方程
    global NP
    global B_WALL, B_INFLOW, B_OUTFLOW, B_SYMMETRY, B_SOURCE, PMAX, EMAX, NVEX, MAX_NITERATION, UNITEC, MOLNUM
    global NP, NE, NPOCH, NOD, NOE, PX, PY
    global CTRL_AREA, TOTAL_AREA
    global EFVM, PFVM, BFVM, AFVM, CFVM
    global CCAJSR, NEWCCA, MEDCCA, RITER, PITER, APK
    global DT, NSTEP, ILOAD, RELEASE_TIMES
    global DSAVE
    global KDCSQ, DCAJSR, BCSQ, H_JSR
    global CCAMYO, DCARYR
    global CCAFSR, DCAFSR
    global ICARYR, ICAFSR, AVG_CA_JSR
    print("PREESTIMATE_EQUATION NP", NP)
    # print("构建n+ 1/2步的方程")
    I = 0
    COEFF = 0.0
    for I in range(0, NP + 1):
        COEFF = CTRL_AREA[I] * (1 + BCSQ * KDCSQ / ((KDCSQ + CCAJSR[I]) ** 2)) / (0.5 * DT * DCAJSR)
        BFVM[I] = COEFF * CCAJSR[I] + CFVM[I]  # 方程中的系数
        AFVM[I] = COEFF + PFVM[I]  # 方程中的系数
        NEWCCA[I] = CCAJSR[I]
    # ---------------------------------------------------------
    CONJUGATED_GRADIENT_SOLUTION()  # 解那两个方程
    for I in range(0, NP + 1):
        MEDCCA[I] = NEWCCA[I]


# *****************************************************
def CORRECTION_EQUATION():  # 构建第n步的方程
    global NP
    global B_WALL, B_INFLOW, B_OUTFLOW, B_SYMMETRY, B_SOURCE, PMAX, EMAX, NVEX, MAX_NITERATION, UNITEC, MOLNUM
    global NP, NE, NPOCH, NOD, NOE, PX, PY
    global CTRL_AREA, TOTAL_AREA
    global EFVM, PFVM, BFVM, AFVM, CFVM
    global CCAJSR, NEWCCA, MEDCCA, RITER, PITER, APK
    global DT, NSTEP, ILOAD, RELEASE_TIMES
    global DSAVE
    global KDCSQ, DCAJSR, BCSQ, H_JSR
    global CCAMYO, DCARYR
    global CCAFSR, DCAFSR
    global ICARYR, ICAFSR, AVG_CA_JSR
    # print("构建第n步的方程")
    I = 0
    N1 = 0
    N2 = 0
    N3 = 0
    COEFF = 0.0
    for I in range(0, NP + 1):
        COEFF = CTRL_AREA[I] * (1 + BCSQ * KDCSQ / ((KDCSQ + MEDCCA[I]) ** 2)) / (0.5 * DT * DCAJSR)
        BFVM[I] = (COEFF - PFVM[I]) * CCAJSR[I] + CFVM[I] + CFVM[I]  # 方程中的系数
        AFVM[I] = COEFF + PFVM[I]  # 方程中的系数
    for I in range(0, NE):
        N1 = NOD[0, I]  # 这些节点组成的三角形单元的信息分别赋值给N1,N2,N3
        N2 = NOD[1, I]
        N3 = NOD[2, I]
        BFVM[N1] = BFVM[N1] - EFVM[0, I] * CCAJSR[N2] - EFVM[2, I] * CCAJSR[N3]
        BFVM[N2] = BFVM[N2] - EFVM[0, I] * CCAJSR[N1] - EFVM[1, I] * CCAJSR[N3]
        BFVM[N3] = BFVM[N3] - EFVM[2, I] * CCAJSR[N1] - EFVM[1, I] * CCAJSR[N2]
    CONJUGATED_GRADIENT_SOLUTION()  # 解那两个方程
    # print("CORRECTION_EQUATION()")


# *****************************************
def CONJUGATED_GRADIENT_SOLUTION():  # 解那两个方程
    global NP
    global B_WALL, B_INFLOW, B_OUTFLOW, B_SYMMETRY, B_SOURCE, PMAX, EMAX, NVEX, MAX_NITERATION, UNITEC, MOLNUM
    global NP, NE, NPOCH, NOD, NOE, PX, PY
    global CTRL_AREA, TOTAL_AREA
    global EFVM, PFVM, BFVM, AFVM, CFVM
    global CCAJSR, NEWCCA, MEDCCA, RITER, PITER, APK
    global DT, NSTEP, ILOAD, RELEASE_TIMES
    global DSAVE
    global KDCSQ, DCAJSR, BCSQ, H_JSR
    global CCAMYO, DCARYR
    global CCAFSR, DCAFSR
    global ICARYR, ICAFSR, AVG_CA_JSR
    # print("调用CONJUGATED_GRADIENT_SOLUTION()方法，解那两个方程")
    N = 0
    I = 0
    N1 = 0
    N2 = 0
    N3 = 0
    QUP = 0.0
    QDOWN = 0.0
    QK = 0.0
    EUP = 0.0
    EDOWN = 0.0
    EK = 0.0
    MAX_ERROR = 0.0
    P_ERROR = 0.0

    for I in range(0, NP + 1):
        RITER[I] = BFVM[I] - AFVM[I] * NEWCCA[I]
    for I in range(0, NE):
        N1 = NOD[0, I]
        N2 = NOD[1, I]
        N3 = NOD[2, I]
        # if N1==1 or N2==1 or N3==1:
        #     print(N1,N2,N3)      
        #     print(RITER[N1],EFVM[0, I],NEWCCA[N2],EFVM[2,I],NEWCCA[N3])
        #     print(RITER[N2],EFVM[0, I],NEWCCA[N1],EFVM[1,I],NEWCCA[N3])
        #     print(RITER[N3],EFVM[2, I],NEWCCA[N1],EFVM[1,I],NEWCCA[N2])
        # print(RITER,RITER[N1],NEWCCA[N2])
        RITER[N1] = RITER[N1] - EFVM[0, I] * NEWCCA[N2] - EFVM[2, I] * NEWCCA[N3]  # 临时数组
        RITER[N2] = RITER[N2] - EFVM[0, I] * NEWCCA[N1] - EFVM[1, I] * NEWCCA[N3]
        RITER[N3] = RITER[N3] - EFVM[2, I] * NEWCCA[N1] - EFVM[1, I] * NEWCCA[N2]
    # --------------------------------------------------------------------------
    for I in range(0, NP + 1):
        PITER[I] = RITER[I]  # 临时数组
    EUP = 0.0
    for I in range(0, NP + 1):
        EUP = EUP + RITER[I] * RITER[I]
    # -------------------------------------------------
    for N in range(0, MAX_NITERATION):
        for I in range(0, NP + 1):
            APK[I] = AFVM[I] * PITER[I]  # 临时数组

        for I in range(0, NE):
            N1 = NOD[0, I]
            N2 = NOD[1, I]
            N3 = NOD[2, I]
            APK[N1] = APK[N1] + EFVM[0, I] * PITER[N2] + EFVM[2, I] * PITER[N3]
            APK[N2] = APK[N2] + EFVM[0, I] * PITER[N1] + EFVM[1, I] * PITER[N3]
            APK[N3] = APK[N3] + EFVM[2, I] * PITER[N1] + EFVM[1, I] * PITER[N2]
        QUP = EUP
        QDOWN = 0.0
        for I in range(0, NP + 1):
            QDOWN = QDOWN + APK[I] * PITER[I]
        # if QDOWN > 0:
        QK = QUP / QDOWN
        # ---------------------------------------------
        for I in range(0, NP + 1):
            NEWCCA[I] = NEWCCA[I] + QK * PITER[I]
            RITER[I] = RITER[I] - QK * APK[I]  # 临时数组

        MAX_ERROR = 0.0
        for I in range(0, NP + 1):
            # if NEWCCA[I] != 0:
            P_ERROR = abs(QK * PITER[I] / NEWCCA[I])
            if MAX_ERROR < P_ERROR:
                MAX_ERROR = P_ERROR
        if MAX_ERROR < (10 ** -5) and N >= 50:
            print('return')
            return

        EUP = 0.0
        for I in range(0, NP + 1):
            EUP = EUP + RITER[I] * RITER[I]
        EDOWN = QDOWN
        # if EDOWN > 0:
        EK = EUP / EDOWN
        # print('N',N)
        for I in range(0, NP + 1):
            PITER[I] = RITER[I] + EK * PITER[I]
    print('466', NEWCCA)

    # print("CONJUGATED_GRADIENT_SOLUTION(123)")


# ********************************************************
def COEFFICIENT():
    global NP
    global B_WALL, B_INFLOW, B_OUTFLOW, B_SYMMETRY, B_SOURCE, PMAX, EMAX, NVEX, MAX_NITERATION, UNITEC, MOLNUM
    global NP, NE, NPOCH, NOD, NOE, PX, PY
    global CTRL_AREA, TOTAL_AREA
    global EFVM, PFVM, BFVM, AFVM, CFVM
    global CCAJSR, NEWCCA, MEDCCA, RITER, PITER, APK
    global DT, NSTEP, ILOAD, RELEASE_TIMES
    global DSAVE
    global KDCSQ, DCAJSR, BCSQ, H_JSR
    global CCAMYO, DCARYR
    global CCAFSR, DCAFSR
    global ICARYR, ICAFSR, AVG_CA_JSR
    # print("开始生成离散化的系数")
    global TOTAL_AREA
    E = 0
    I = 0
    J = 0
    K = 0
    N1 = 0
    N2 = 0
    N3 = 0
    VOL6 = 0.0
    VOL = 0.0
    # TOTAL_VOL = 0.0
    MATRIX0 = np.zeros((3, 3), float)
    MATRIX1 = np.zeros((3, 3), float)
    MATRIX2 = np.zeros((3, 3), float)
    MATRIX4 = np.zeros((2, 2), float)
    VER1 = np.zeros(2, float)
    VER2 = np.zeros(2, float)
    BE = np.zeros(3, float)
    CE = np.zeros(3, float)
    LENGTH = 0.0
    TOTAL_VOL = 0.0
    for I in range(0, NP + 1):
        PFVM[I] = 0.0
        AFVM[I] = 0.0
        BFVM[I] = 0.0
        CFVM[I] = 0.0
        CTRL_AREA[I] = 0
    for E in range(0, NE):  # NE为三角形单元的数量
        N1 = NOD[0, E]
        N2 = NOD[1, E]
        N3 = NOD[2, E]

        for I in range(0, 3):
            MATRIX1[I, 0] = 1.0
            MATRIX1[I, 1] = PX[NOD[I, E]]
            MATRIX1[I, 2] = PY[NOD[I, E]]
        for I in range(0, 3):
            for J in range(0, 3):
                MATRIX0[I, J] = MATRIX1[I, J]
        VOL6 = DET(MATRIX1, 3, VOL6)  # 用于计算时间dt

        VOL = VOL6 / 2.0
        TOTAL_VOL = TOTAL_VOL + VOL
        # print('VOL6',VOL6,E)
        for I in range(0, 3):
            CTRL_AREA[NOD[I, E]] = CTRL_AREA[NOD[I, E]] + VOL

        for I in range(0, 3):
            for J in range(0, 3):
                for K in range(0, 3):
                    MATRIX2[J, K] = MATRIX0[J, K]
            for J in range(1, 3):
                MATRIX2[I, J] = MATRIX0[2, J]
            for J in range(0, 2):
                MATRIX2[J, 1] = MATRIX2[J, 1] - PX[NOD[I, E]]
                MATRIX2[J, 2] = MATRIX2[J, 2] - PY[NOD[I, E]]

            for J in range(0, 2):
                VER1[J] = -1.0
            for J in range(0, 2):
                for K in range(0, 2):
                    MATRIX4[J, K] = MATRIX2[J, K + 1]
            AXEQB(MATRIX4, VER1, 2, VER2)
            # print('VER1,VER22',VER1,VER2)
            BE[I] = VER2[0]
            CE[I] = VER2[1]

        #  A(N1,N2) = A(N2, N1)
        EFVM[0, E] = (CE[1] * (PX[N3] - PX[N2]) - BE[1] * (PY[N3] - PY[N2]) + CE[0] * (PX[N1] - PX[N3]) - BE[0] * (
                PY[N1] - PY[N3])) / 2.0

        #  A(N2,N3) = A(N3, N2)
        EFVM[1, E] = (CE[1] * (PX[N2] - PX[N1]) - BE[1] * (PY[N2] - PY[N1]) + CE[2] * (PX[N1] - PX[N3]) - BE[2] * (
                PY[N1] - PY[N3])) / 2.0
        #  A(N3,N1) = A(N1, N3)
        EFVM[2, E] = (CE[2] * (PX[N3] - PX[N2]) - BE[2] * (PY[N3] - PY[N2]) + CE[0] * (PX[N2] - PX[N1]) - BE[0] * (
                PY[N2] - PY[N1])) / 2.0

        PFVM[N1] = PFVM[N1] + CE[0] * (PX[N3] - PX[N2]) - BE[0] * (PY[N3] - PY[N2])
        PFVM[N2] = PFVM[N2] + CE[1] * (PX[N1] - PX[N3]) - BE[1] * (PY[N1] - PY[N3])
        PFVM[N3] = PFVM[N3] + CE[2] * (PX[N2] - PX[N1]) - BE[2] * (PY[N2] - PY[N1])
        # *** OUTFLOW

        if NPOCH[N2] == B_OUTFLOW and NPOCH[N3] == B_OUTFLOW:
            LENGTH = sqrt((PY[N3] - PY[N2]) ** 2 + (PX[N3] - PX[N2]) ** 2)
            PFVM[N1] = PFVM[N1] + DCARYR * LENGTH / DCAJSR
            PFVM[N2] = PFVM[N2] + DCARYR * LENGTH / DCAJSR
            PFVM[N3] = PFVM[N3] + DCARYR * LENGTH / DCAJSR
            # print('PFVM',N1,N2,N3,PFVM[N1],PFVM[N2],PFVM[N3])
        if NPOCH[N1] == B_OUTFLOW and NPOCH[N3] == B_OUTFLOW:
            LENGTH = sqrt((PY[N3] - PY[N1]) ** 2 + (PX[N3] - PX[N1]) ** 2)
            PFVM[N1] = PFVM[N1] + DCARYR * LENGTH / DCAJSR
            PFVM[N2] = PFVM[N2] + DCARYR * LENGTH / DCAJSR
            PFVM[N3] = PFVM[N3] + DCARYR * LENGTH / DCAJSR
        if NPOCH[N2] == B_OUTFLOW and NPOCH[N1] == B_OUTFLOW:
            LENGTH = sqrt((PY[N1] - PY[N2]) ** 2 + (PX[N1] - PX[N2]) ** 2)
            PFVM[N3] = PFVM[N3] + DCARYR * LENGTH / DCAJSR
            PFVM[N2] = PFVM[N2] + DCARYR * LENGTH / DCAJSR
            PFVM[N1] = PFVM[N1] + DCARYR * LENGTH / DCAJSR
        #  INFLOW

        if NPOCH[N2] == B_INFLOW and NPOCH[N3] == B_INFLOW:
            LENGTH = sqrt((PY[N3] - PY[N2]) ** 2 + (PX[N3] - PX[N2]) ** 2)
            PFVM[N1] = PFVM[N1] + DCAFSR * LENGTH / DCAJSR
            PFVM[N2] = PFVM[N2] + DCAFSR * LENGTH / DCAJSR
            PFVM[N3] = PFVM[N3] + DCAFSR * LENGTH / DCAJSR
            CFVM[N1] = CFVM[N1] + CCAFSR * DCAFSR * LENGTH / DCAJSR
            CFVM[N2] = CFVM[N2] + CCAFSR * DCAFSR * LENGTH / DCAJSR
            CFVM[N3] = CFVM[N3] + CCAFSR * DCAFSR * LENGTH / DCAJSR
        if NPOCH[N1] == B_INFLOW and NPOCH[N3] == B_INFLOW:
            LENGTH = sqrt((PY[N3] - PY[N1]) ** 2 + (PX[N3] - PX[N1]) ** 2)
            PFVM[N1] = PFVM[N1] + DCAFSR * LENGTH / DCAJSR
            PFVM[N2] = PFVM[N2] + DCAFSR * LENGTH / DCAJSR
            PFVM[N3] = PFVM[N3] + DCAFSR * LENGTH / DCAJSR
            CFVM[N1] = CFVM[N1] + CCAFSR * DCAFSR * LENGTH / DCAJSR
            CFVM[N2] = CFVM[N2] + CCAFSR * DCAFSR * LENGTH / DCAJSR
            CFVM[N3] = CFVM[N3] + CCAFSR * DCAFSR * LENGTH / DCAJSR
        if NPOCH[N2] == B_INFLOW and NPOCH[N1] == B_INFLOW:
            LENGTH = sqrt((PY[N1] - PY[N2]) ** 2 + (PX[N1] - PX[N2]) ** 2)
            PFVM[N1] = PFVM[N1] + DCAFSR * LENGTH / DCAJSR
            PFVM[N2] = PFVM[N2] + DCAFSR * LENGTH / DCAJSR
            PFVM[N3] = PFVM[N3] + DCAFSR * LENGTH / DCAJSR
            CFVM[N1] = CFVM[N1] + CCAFSR * DCAFSR * LENGTH / DCAJSR
            CFVM[N2] = CFVM[N2] + CCAFSR * DCAFSR * LENGTH / DCAJSR
            CFVM[N3] = CFVM[N3] + CCAFSR * DCAFSR * LENGTH / DCAJSR

    TOTAL_AREA = TOTAL_VOL * 3
    # **************************************************
    # print("COEFFICIENT()")


def LOAD_GRIDINFO():
    global NP
    global B_WALL, B_INFLOW, B_OUTFLOW, B_SYMMETRY, B_SOURCE, PMAX, EMAX, NVEX, MAX_NITERATION, UNITEC, MOLNUM
    global NP, NE, NPOCH, NOD, NOE, PX, PY
    global CTRL_AREA, TOTAL_AREA
    global EFVM, PFVM, BFVM, AFVM, CFVM
    global CCAJSR, NEWCCA, MEDCCA, RITER, PITER, APK
    global DT, NSTEP, ILOAD, RELEASE_TIMES
    global DSAVE
    global KDCSQ, DCAJSR, BCSQ, H_JSR
    global CCAMYO, DCARYR
    global CCAFSR, DCAFSR
    global ICARYR, ICAFSR, AVG_CA_JSR
    # print("调用LOAD_GRIDINFO()方法，加载网格信息")
    # ?????????????
    global NP, NE
    I = 0
    count = 0
    gridt_file = open('gridt.dat', 'r')  # gridt.dat，这个是空间离散化的每一个离散的节点的坐标，第一行是节点的数量
    for line in gridt_file.readlines():  # 把空间里面离散的每一点的坐标的横坐标和纵坐标分别加载到PX数组和PY数组，把结点的数量存入到NP中
        current_line = list(filter(not_empty, line.strip("\n").split(" ")))
        PX[count] = current_line[0]
        PY[count] = current_line[1]
        # print(PX[count], PY[count])
        count = count + 1
    NP = count - 1

    print('PX[522],PX[486]', PX[522], PX[486])
    gridt_file.close()
    # I = 0
    # GRI = open('gridt.dat', "rb+")
    # NP = GRI.read(1)
    # # NP_INT = int.from_bytes(NP, byteorder='little', signed=True)
    # for I in range(0, NP):
    #     PX[I], PY[I] = GRI.read(2)
    # GRI.close()
    count = 0
    gridt_file = open('npoch.dat', 'r')  # npoch.dat为每个节点的属性：0代表内部节点，1代表入流边界或远场的节点，2代表壁面的节点，4代表出流边界节点
    for line in gridt_file.readlines():  # 把每个结点的属性存入到NPOCH数组中
        current_line = list(filter(not_empty, line.strip("\n").split(" ")))
        NPOCH[count] = current_line[0]
        # print(NPOCH[count])
        count = count + 1
    gridt_file.close()
    # NPO = open("npoch.dat", "rb+")
    # NPO1 = NPO.read(1)
    # # NPO1_INT = int.from_bytes(NPO1, byteorder='little', signed=True)
    # for I in range(0, NP):
    #     NPOCH[I] = int.from_bytes(NPO.read(1), byteorder='little', signed=True)
    # NPO.close()

    count = 0
    gridt_file = open('nod.dat', 'r')  # nod.dat，这个是gridt.dat中这些节点组成的三角形单元的信息，第一行是三角形单元的数量，后面是每一个三角元对应的三个节点的编号；
    for line in gridt_file.readlines():  # 把每一个三角形单元所对应的三角形单元的编号分别存入到数组NOD中，即NOD是每个三角形单元所对应的节点编号的数组
        current_line = list(filter(not_empty, line.strip("\n").split(" ")))
        NOD[0, count] = int(current_line[0]) - 1
        NOD[1, count] = int(current_line[1]) - 1
        NOD[2, count] = int(current_line[2]) - 1
        # print(NOD[0, count], NOD[1, count], NOD[2, count])
        count = count + 1
    NE = count  # NE为三角形单元的数量
    gridt_file.close()
    # NO1 = open("nod.dat", "rb+")
    # NE = NO1.read(1)
    # # NE_INT = int.from_bytes(NP, byteorder='little', signed=True)
    # for I in range(0, NE):
    #     NOD[0, I], NOD[1, I], NOD[2, I] = NO1.read(3)
    # NO1.close()
    # print("读取文件noe的数据存入NOE数组")
    count = 0
    gridt_file = open('noe.dat', 'r')  # noe.dat，这个是每一个三角形单元的三个邻居单元的编号（所谓邻居指的是和这个单元有一条边重合的三角形单元），编号0表示这条边是区域边界，所以没有邻居
    for line in gridt_file.readlines():  # 把每一个三角形单元所对应的邻居单元的编号存入到数组NOE中
        current_line = list(filter(not_empty, line.strip("\n").split(" ")))
        NOE[0, count] = int(current_line[0]) - 1
        NOE[1, count] = int(current_line[1]) - 1
        NOE[2, count] = int(current_line[2]) - 1
        # print(NOE[0, count], NOE[1, count], NOE[2, count])
        count = count + 1
    gridt_file.close()
    # print("读取文件noe的数据存入NOE数组完毕")
    # NO2 = open("noe.dat", "rb+")
    # for i in range(0, NE):
    #     NOE[0, I], NOE[1, I], NOE[2, I] = NO2.read(3)
    # NO2.close()
    # print("LOAD_GRIDINFO()")


# *******************************************************
def DET(MATRI, NUM, DET_MATRI):  # 解那两个方程，计算dt的值
    global NP
    global B_WALL, B_INFLOW, B_OUTFLOW, B_SYMMETRY, B_SOURCE, PMAX, EMAX, NVEX, MAX_NITERATION, UNITEC, MOLNUM
    global NP, NE, NPOCH, NOD, NOE, PX, PY
    global CTRL_AREA, TOTAL_AREA
    global EFVM, PFVM, BFVM, AFVM, CFVM
    global CCAJSR, NEWCCA, MEDCCA, RITER, PITER, APK
    global DT, NSTEP, ILOAD, RELEASE_TIMES
    global DSAVE
    global KDCSQ, DCAJSR, BCSQ, H_JSR
    global CCAMYO, DCARYR
    global CCAFSR, DCAFSR
    global ICARYR, ICAFSR, AVG_CA_JSR
    # print("DET(MATRI, NUM, DET_MATRI)")
    # NUM = 0
    # print("调用DET()方法，解那两个方程，计算dt的值")
    I = 0
    J = 0
    K = 0
    # SIGN_1 = 0
    # DET_MATRI = 0.0
    # DET_MATRIX = 0.0
    REAL_1 = 0.0
    REAL_2 = 0.0
    # MATRI = np.empty([NUM, NUM], float)
    MATRIX = np.zeros([NUM, NUM])  # 3*3矩阵

    for I in range(0, NUM):
        for J in range(0, NUM):
            MATRIX[I, J] = MATRI[I, J]
    DET_MATRIX = 1
    SIGN_1 = 1
    for I in range(0, NUM - 1):
        REAL_1 = MATRIX[I, I]
        for J in range(I + 1, NUM):
            if abs(MATRIX[J, I]) > abs(REAL_1):
                for K in range(I, NUM):
                    REAL_1 = MATRIX[I, K]
                    MATRIX[I, K] = MATRIX[J, K]
                    MATRIX[J, K] = REAL_1
                SIGN_1 = SIGN_1 * (-1)
            REAL_1 = MATRIX[I, I]
        REAL_1 = MATRIX[I, I]
        if abs(REAL_1) < 10 ** (-8):
            DET_MATRI = 0.0
            return
        MATRIX[I, I] = 1.0
        DET_MATRIX = DET_MATRIX * REAL_1

        for J in range(I + 1, NUM):
            REAL_2 = MATRIX[J, I] / REAL_1

            MATRIX[J, I] = 0.0
            for K in range(I + 1, NUM):
                MATRIX[J, K] = MATRIX[J, K] - REAL_2 * MATRIX[I, K]
    DET_MATRIX = DET_MATRIX * MATRIX[NUM - 1, NUM - 1] * SIGN_1
    # print(DET_MATRIX,MATRIX[NUM - 1, NUM - 1])
    # ????????
    return DET_MATRIX
    # print('DET_MATRI',DET_MATRI)
    # print("DET(MATRI, NUM, DET_MATRI)")


# ***********************************************
def AXEQB(ARR1, VERB1, NUM, VERX1):  # 解那两个方程
    global NP
    global B_WALL, B_INFLOW, B_OUTFLOW, B_SYMMETRY, B_SOURCE, PMAX, EMAX, NVEX, MAX_NITERATION, UNITEC, MOLNUM
    global NP, NE, NPOCH, NOD, NOE, PX, PY
    global CTRL_AREA, TOTAL_AREA
    global EFVM, PFVM, BFVM, AFVM, CFVM
    global CCAJSR, NEWCCA, MEDCCA, RITER, PITER, APK
    global DT, NSTEP, ILOAD, RELEASE_TIMES
    global DSAVE
    global KDCSQ, DCAJSR, BCSQ, H_JSR
    global CCAMYO, DCARYR
    global CCAFSR, DCAFSR
    global ICARYR, ICAFSR, AVG_CA_JSR
    # print("AXEQB(ARR1, VERB1, NUM, VERX1)")
    # NUM = 0
    # ARR1 = np.empty([NUM, NUM], float)
    # print("调用AXEQB()方法，解那两个方程")
    ARR = np.empty([NUM, NUM], float)

    # VERB1 = np.empty(NUM, float)
    # VERX1 = np.empty(NUM, float)
    VERB = np.empty(NUM, float)
    VERX = np.empty(NUM, float)
    I = 0
    J = 0
    K = 0
    REAL_1 = 0.0
    REAL_2 = 0.0
    for I in range(0, NUM):
        for J in range(0, NUM):
            ARR[I, J] = ARR1[I, J]
        VERB[I] = VERB1[I]
    for I in range(0, NUM - 1):
        REAL_1 = ARR[I, I]
        for J in range(I + 1, NUM):
            if abs(ARR[J, I]) > abs(REAL_1):
                for K in range(I, NUM):
                    REAL_1 = ARR[I, K]
                    ARR[I, K] = ARR[J, K]
                    ARR[J, K] = REAL_1
                REAL_1 = VERB[I]
                VERB[I] = VERB[J]
                VERB[J] = REAL_1
            REAL_1 = ARR[I, I]
        # print('ARR',ARR)没问题
        REAL_1 = ARR[I, I]
        ARR[I, I] = 1.0
        if abs(REAL_1) < (10 ** -8):
            print("DET(ARR)=0,THIS EQUATION NO ANSWER")
            print(ARR1)
            return
        for J in range(I + 1, NUM):
            ARR[I, J] = ARR[I, J] / REAL_1
        VERB[I] = VERB[I] / REAL_1

        for J in range(I + 1, NUM):
            REAL_2 = ARR[J, I]
            ARR[J, I] = 0.0
            for K in range(I + 1, NUM):
                ARR[J, K] = ARR[J, K] - REAL_2 * ARR[I, K]
            VERB[J] = VERB[J] - REAL_2 * VERB[I]

    # ?????????
    if abs(ARR[NUM - 1, NUM - 1]) < 10 ** -8:
        print("DET(ARR)=0,THIS EQUATION NO ANSWER")
        print(ARR1)
        return
    VERX[NUM - 1] = VERB[NUM - 1] / ARR[NUM - 1, NUM - 1]

    for I in range(NUM - 2, -1, -1):
        VERX[I] = VERB[I]
        for J in range(NUM - 1, I, -1):
            VERX[I] = VERX[I] - ARR[I, J] * VERX[J]
    for I in range(0, NUM):
        VERX1[I] = VERX[I]

    # print("AXEQB(ARR1, VERB1, NUM, VERX1)")


# ********************************************

main()
