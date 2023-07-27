import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
from matplotlib import rc
import scienceplots
# from matplotlib.legend_handler import HandlerLine2D
rc('text', usetex=True)
plt.style.use(['science']) # style used in scientific papers(LaTeX based)

eta1 = 3.0
eta2 = 1.1
eta3 = 0.3

def func(x):
    return [x[0]*(1 + np.abs(x[0]-x[1])) - eta1, x[1]*(eta3 + np.abs(x[0]-x[1])) - eta2]

x0 = np.array([2.5,2.5])
T = np.empty((1,))
S = np.empty((1,))
param = np.empty((1,))

while eta2 < 2.1:
    root = fsolve(func,x0)
    T = np.append(T,root[0])
    S = np.append(S,root[1])
    param = np.append(param,eta2)
    eta2 += 0.005

fig, axs = plt.subplots(figsize=(8,5))

T, = axs.plot(param[1:], T[1:],linestyle='solid',linewidth=1.,color="lime")
S, = axs.plot(param[1:], S[1:],color='dodgerblue',linestyle='solid',linewidth=1.)

axs.set_xlim(0,2)
# axs.set_ylim(0,1.5)
axs.set_title(r'Diagramma di biforcazione',fontsize=9)
axs.set_xlabel('$\eta_2$',fontsize=9)
axs.set_ylabel('$T,S$',fontsize=9)
axs.grid(visible=True, which='major', color='0.8', linestyle='-')
axs.grid(visible=True, which='minor', color='gray', linestyle='dotted', alpha=0.2)
axs.minorticks_on()

axs.legend((T,S),
           ('T', 'S'),
           loc='best',
           ncol=1,
           fontsize=9)
# axs.text(2,2,
#          '$\eta_2 = 1.0$',
#          fontsize = 10,
#          bbox = dict(boxstyle="round,pad=0.6",facecolor = 'white', alpha = 0.5,edgecolor='None'))
plt.savefig('../figs/bifurcation1.pdf')
