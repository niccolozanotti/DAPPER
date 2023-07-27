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
def f(q, param):
    return q - eta1 / (1+np.abs(q)) + param / (eta3+np.abs(q))
def T(q):
    return eta1/(1+ np.abs(q))
def S(q, param):
    return param/(eta3+ np.abs(q))

q  = np.linspace(-1.5,1.5,30000)
q =.5*q[1:]+.5*q[:-1]

print('n.roots',' ','eta2')
while eta2 <= 2.1:
    fq = f(q[1:],eta2)*f(q[:-1],eta2)
    roots = [q1 for q1,f1 in zip(q,fq) if f1<0.]
    print(len(roots),'\t',eta2)
    eta2 += 0.01