import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import scienceplots
# from matplotlib.legend_handler import HandlerLine2D
rc('text', usetex=True)
plt.style.use(['science']) # style used in scientific papers(LaTeX based)

eta1 = 3.0
eta2 = 0.0 # starting value
eta3 = 0.3
L1 = eta1*eta3
#Function of transport that is equal to zero in equilibrium.
def f(q, param):
    return q - eta1 / (1+np.abs(q)) + param / (eta3+np.abs(q))
def T(q):
    return eta1/(1+ np.abs(q))
def S(q, param):
    return param/(eta3+ np.abs(q))


q = np.linspace(-1.5,1.5,30000)
q = .5*q[1:]+.5*q[:-1]

# vector containing equilibrium flux values and T,S and values of parameters
state = np.array([[0.0],[0.0],[0.0],[0.0],[0.0],[0.0]]) # in order: psi, T , S , eta1, eta2, eta3

while eta2 <= 2.1:
    fq = f(q[1:],eta2)*f(q[:-1],eta2)
    roots = [q1 for q1,f1 in zip(q,fq) if f1<0.]
    if len(roots) > 1 :
        print('eta2 = ',eta2,'\tn. sol=',len(roots))
        for i in range(len(roots)):
            state = np.append(state, [[roots[i]],[T(roots[i])],[S(roots[i],eta2)], [eta1], [eta2], [eta3]],axis=1)
    else:
        state = np.append(state, [[roots[0]],[T(roots[0])], [S(roots[0],eta2)],[eta1],[eta2],[eta3]],axis=1)
    eta2 += 0.0005

fig, axs = plt.subplots(figsize=(8,5))

T = axs.scatter(state[4,1:],state[1,1:],marker='.',s=1.2,color="black")
S = axs.scatter(state[4,1:],state[2,1:],marker='.',s=1.2,color='violet')

axs.set_xlim(0,2.1)
axs.set_ylim(0,3.2)
axs.set_title(r'Diagramma di biforcazione',fontsize=10)
axs.set_xlabel('$\eta_2$',fontsize=9)
axs.set_ylabel('$T,S$',fontsize=9)
# axs.grid(visible=True, which='major', color='0.8', linestyle='-')
# axs.grid(visible=True, which='minor', color='gray', linestyle='dotted', alpha=0.2)
axs.minorticks_on()

axs.legend((T,S),
           ('T', 'S'),
           loc='best',
           ncol=1,
           fontsize=12)
plt.vlines(x = 0.9, ymin = 0, ymax= 3.2,
           colors = 'black',linestyles='dashed',
           label = '$L_1$')
# plt.axvline(x=1.22, color='lightgray')
plt.vlines(x = 1.22, ymin = 0, ymax= 3.2,
           colors = 'black',linestyles='dashed',
           label = '$L_2$')
ann = axs.annotate("$L_1$",
                  xy=(0.89, 3), xycoords='data',
                  xytext=(0.75,2.5), textcoords='data',
                  size=10, va="center", ha="center",
                  arrowprops=dict(arrowstyle="-|>",
                                  connectionstyle="arc3,rad=-0.2",
                                  fc="w"))
ann = axs.annotate("$L_2$",
                  xy=(1.25,1.7), xycoords='data',
                  xytext=(1.45,1.7), textcoords='data',
                  size=10, va="center", ha="center",
                  arrowprops=dict(arrowstyle="-|>",
                                  connectionstyle="arc3,rad=-0.2",
                                  fc="w"))
# axs.text(2,2,
#          '$\eta_2 = 1.0$',
#          fontsize = 10,
#          bbox = dict(boxstyle="round,pad=0.6",facecolor = 'white', alpha = 0.5,edgecolor='None'))
plt.savefig('../figs/roots-bifurcation.pdf')
