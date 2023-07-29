# regime diagram Dijkstra p.385
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import scienceplots
# from matplotlib.legend_handler import HandlerLine2D
rc('text', usetex=True)
plt.style.use(['science']) # style used in scientific papers(LaTeX based)

# eta1 = 3.0 # starting value --> up to 5.0
# eta2 = 0.0 # starting value --> up to 2.0
eta3 = 0.3
step_eta1 = 0.002
step_eta2 = 0.002
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

eta1 = 0.01
while eta1 <= 5.0:  # we know the val is < 1.0
    L1 = calc_L1(eta1)
    L2 = calc_L2(eta1,q)
    state = np.append(state, [[L1], [L2], [eta1]],axis=1)
    print('eta1 =',eta1,'\tL1=',L1,'\tL2',L2)
    eta1 += step_eta1

# Plotting
fig, axs = plt.subplots(figsize=(8,5))

L1, = plt.plot(state[2,1:],state[0,1:],linestyle='solid',linewidth= 0.9,color='black') # L2
L2, = plt.plot(state[2,1:],state[1,1:],linestyle='solid',linewidth= 0.9,color='violet') # L1

axs.set_xlim(0,5)
axs.set_ylim(0,2.0)
# axs.set_title(r'Diagramma di regime',fontsize=13)
axs.set_xlabel('$\eta_1$',fontsize=13)
axs.set_ylabel('$\eta_2$',fontsize=13)
# axs.grid(visible=True, which='major', color='0.8', linestyle='-')
# axs.grid(visible=True, which='minor', color='gray', linestyle='dotted', alpha=0.2)
axs.minorticks_on()
#
axs.legend((L1,L2),
           ('$L_1$', '$L_2$'),
           loc='best',
           ncol=1,
           fontsize=13)
axs.text(1.1,1.35,
         'SA',
         fontsize = 13,
         bbox = dict(boxstyle="round,pad=0.6",facecolor = 'white', alpha = 0.5,edgecolor='None'))
axs.text(4.0,0.5,
         'TH',
         fontsize = 13,
         bbox = dict(boxstyle="round,pad=0.6",facecolor = 'white', alpha = 0.5,edgecolor='None'))
axs.text(4.22,1.62,
         'TH+SA',
         fontsize = 13,
         bbox = dict(boxstyle="round,pad=0.6",facecolor = 'white', alpha = 0.5,edgecolor='None'))
plt.savefig('../figs/regime-diagram.pdf')
