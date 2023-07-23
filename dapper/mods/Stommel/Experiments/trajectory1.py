# Integration of the model equations using Runge-Kutta 4-th order scheme
import numpy as np

def RK4_step(f,t,y,h):
    k1 = h*f(t,y)
    k2 = h*f(t+0.5*h, y+0.5*k1)
    k3 = h*f(t+0.5*h, y+0.5*k2)
    k4 = h*f(t+h, y+k3)
    return y+(k1 + 2*k2 + 2*k3 + k4)/6

#parameters of the model
eta_1 = 3.0
eta_2 = 0.5
eta_3 = 0.3

def Stommel2box(t,v):
    #setting up vector v = (T,S)
    dv_dt = 0*v
    dv_dt[0] = eta_1 - v[0]*(1 + np.abs(v[0]-v[1]))
    dv_dt[1] = eta_2 - v[1]*(eta_3 + np.abs(v[0]-v[1]))
    return dv_dt


#define the given range t
t0=0
tn=10
h=0.05

#define number of steps (n)

time = np.arange(t0, tn, h)
v = np.zeros([len(time),2],float)

# initial values
v[0,0] = 0.0  # initial temperature difference
v[0,1] = 0.0  # initial salinity difference

# solve
for i in range(len(time)-1):
  v[i+1] = RK4_step(Stommel2box,time[i],v[i],h)

### Plot
import matplotlib.pyplot as plt
from matplotlib import rc
import scienceplots
# from matplotlib.legend_handler import HandlerLine2D
rc('text', usetex=True)
plt.style.use(['science']) # style used in scientific papers(LaTeX based)

###
fig, axs = plt.subplots(figsize=(8,5))

T, = axs.plot(time, v[:,0],linestyle='solid',linewidth=1.,color="violet")
S, = axs.plot(time, v[:,1],color='black',linestyle='solid',linewidth=1.)

axs.set_xlim(0,10)
axs.set_ylim(0,1.5)
# axs.set_title(r'Trajectory',fontsize=9)
axs.set_xlabel('$t$',fontsize=9)
axs.set_ylabel('$T,S$',fontsize=9)
# axs.grid(visible=True, which='major', color='0.8', linestyle='-')
# axs.grid(visible=True, which='minor', color='gray', linestyle='dotted', alpha=0.2)
axs.minorticks_on()

axs.legend((T,S),
           ('$T$', '$S$'),
           loc='best',
           ncol=1,
           fontsize=12)
axs.text(6,0.8,
         '$\eta_2 = 0.5$',
         fontsize = 12,
         bbox = dict(boxstyle="round,pad=0.6",facecolor = 'white', alpha = 0.5,edgecolor='None'))
plt.savefig('../figs/trajectory1.pdf')
###
