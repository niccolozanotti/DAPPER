import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import scienceplots
# from matplotlib.legend_handler import HandlerLine2D
rc('text', usetex=True)
plt.style.use(['science']) # style used in scientific papers(LaTeX based)

eta1 = 0.25
eta2 = 0.0 # starting value
eta3 = 0.3

#Function of transport that is equal to zero in equilibrium.
f = lambda q: (q - eta1 / (1+np.abs(q)) + eta2 / (eta3+np.abs(q)))
T = lambda q: (eta1/ (1 + np.abs(q)))
S = lambda q: (eta2/ (eta3 + np.abs(q)))

#Evaluate values on grid.
q  = np.linspace(-1.5,1.5,30000)
fq = f(q)

q =.5*q[1:]+.5*q[:-1]
fq=fq[1:]*fq[:-1]
roots = [q1 for q1,f1 in zip(q,fq) if f1<0.]

print('n.roots','\t','eta2')
while eta2 <= 2.1:
    roots = [q1 for q1,f1 in zip(q,fq) if f1<0.]
    print(len(roots),'\t',eta2)
    eta2 += 0.01