# regime diagram Dijkstra p.385
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import scienceplots
# from matplotlib.legend_handler import HandlerLine2D
rc('text', usetex=True)
plt.style.use(['science']) # style used in scientific papers(LaTeX based)

eta1 = 3.0 # starting value --> up to 5.0
eta2 = 0.0 # starting value --> up to 2.0
eta3 = 0.3
step_eta1 = 0.01
step_eta2 = 0.01
#Function of transport that is equal to zero in equilibrium.
def f(q, params):
    # params = [eta1,eta2]
    return q - params[0] / (1+np.abs(q)) + params[1] / (eta3+np.abs(q))
def calc_L1(e1):
    return eta3*e1

def calc_L2(e1,q):
    e2 = calc_L1(e1) # starting from L1, there have to be multiple solutions
    i = 0
    while e2 < 2.01:
        params = [e1,e2]
        fq = f(q[1:], params) * f(q[:-1], params)
        q_roots = [q1 for q1, f1 in zip(q, fq) if f1 < 0.]
        if len(q_roots) == 1 and i != 0:
            if i ==1:
                print('L1=L2')
                return e2 - step_eta2
            return e2 - step_eta2
        e2 += step_eta2
        i +=1

q = np.linspace(-3.,3.,30000)
q = .5*q[1:]+.5*q[:-1]

# vector containing equilibrium flux values and T,S and values of parameters
state = np.array([[0.0],[0.0],[0.0]]) # in order: L1, L2 eta1



eta1 = 0.1
while eta1 <= 5.0:  # we know the val is < 1.0
    L1 = calc_L1(eta1)
    L2 = calc_L2(eta1,q)
    state = np.append(state, [[L1], [L2], [eta1]],axis=1)
    print('eta1 =',eta1,'\tL1=',L1,'\tL2',L2)
    eta1 += step_eta1

plt.scatter(state[2,1:],state[1,1:]) # L2
plt.scatter(state[2,1:],state[0,1:]) # L1
plt.show()
# Plotting
# fig, axs = plt.subplots(figsize=(8,5))
#
# T = axs.scatter(state[4,1:],state[1,1:],marker='.',s=1.2,color="black")
# S = axs.scatter(state[4,1:],state[2,1:],marker='.',s=1.2,color='violet')
#
# axs.set_xlim(0,2.1)
# axs.set_ylim(0,3.2)
# axs.set_title(r'Diagramma di biforcazione',fontsize=10)
# axs.set_xlabel('$\eta_2$',fontsize=9)
# axs.set_ylabel('$T,S$',fontsize=9)
# # axs.grid(visible=True, which='major', color='0.8', linestyle='-')
# # axs.grid(visible=True, which='minor', color='gray', linestyle='dotted', alpha=0.2)
# axs.minorticks_on()
#
# axs.legend((T,S),
#            ('T', 'S'),
#            loc='best',
#            ncol=1,
#            fontsize=12)
# plt.vlines(x = 0.9, ymin = 0, ymax= 3.2,
#            colors = 'black',linestyles='dashed',
#            label = '$L_1$')
# # plt.axvline(x=1.22, color='lightgray')
# plt.vlines(x = 1.22, ymin = 0, ymax= 3.2,
#            colors = 'black',linestyles='dashed',
#            label = '$L_2$')
# ann = axs.annotate("$L_1$",
#                   xy=(0.89, 3), xycoords='data',
#                   xytext=(0.75,2.5), textcoords='data',
#                   size=10, va="center", ha="center",
#                   arrowprops=dict(arrowstyle="-|>",
#                                   connectionstyle="arc3,rad=-0.2",
#                                   fc="w"))
# ann = axs.annotate("$L_2$",
#                   xy=(1.25,1.7), xycoords='data',
#                   xytext=(1.45,1.7), textcoords='data',
#                   size=10, va="center", ha="center",
#                   arrowprops=dict(arrowstyle="-|>",
#                                   connectionstyle="arc3,rad=-0.2",
#                                   fc="w"))
# # axs.text(2,2,
# #          '$\eta_2 = 1.0$',
# #          fontsize = 10,
# #          bbox = dict(boxstyle="round,pad=0.6",facecolor = 'white', alpha = 0.5,edgecolor='None'))
# plt.savefig('../figs/regime-diagram.pdf')
