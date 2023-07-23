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
eta_2 = 1.0
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

########################################

time = np.arange(t0, tn, h)
v1 = np.zeros([len(time),2],float)

# initial values
v1[0,0] = 0.0  # initial temperature difference
v1[0,1] = 0.0  # initial salinity difference

# solve
for i in range(len(time)-1):
  v1[i+1] = RK4_step(Stommel2box,time[i],v1[i],h)

time2 = np.arange(t0, tn, h)
v2 = np.zeros([len(time),2],float)

# initial values
v2[0,0] = 2.5  # initial temperature difference
v2[0,1] = 2.5  # initial salinity difference

# solve
for i in range(len(time)-1):
  v2[i+1] = RK4_step(Stommel2box,time2[i],v2[i],h)

time3 = np.arange(t0, tn, h)
v3 = np.zeros([len(time),2],float)

# initial values
v3[0,0] = 3.0  # initial temperature difference
v3[0,1] = 3.0  # initial salinity difference

# solve
for i in range(len(time)-1):
  v3[i+1] = RK4_step(Stommel2box,time3[i],v3[i],h)

#############################################
### Plot
import matplotlib.pyplot as plt
from matplotlib import rc
import scienceplots
# from matplotlib.legend_handler import HandlerLine2D
rc('text', usetex=True)
plt.style.use(['science']) # style used in scientific papers(LaTeX based)

###
fig, axs = plt.subplots(figsize=(8,5))

T1, = axs.plot(time, v1[:,0],linestyle='solid',linewidth=1.,color="violet")
S1, = axs.plot(time, v1[:,1],color='black',linestyle='solid',linewidth=1.)
T2, = axs.plot(time, v2[:,0],linestyle='solid',linewidth=1.,color="violet")
S2, = axs.plot(time, v2[:,1],color='black',linestyle='solid',linewidth=1.)
T3, = axs.plot(time, v3[:,0],linestyle='solid',linewidth=1.,color="violet")
S3, = axs.plot(time, v3[:,1],color='black',linestyle='solid',linewidth=1.)

axs.set_xlim(0,10)
axs.set_ylim(-0.5,3.5)
# axs.set_title(r'Trajectory',fontsize=9)
axs.set_xlabel('$t$',fontsize=9)
axs.set_ylabel('$T,S$',fontsize=9)
# axs.grid(visible=True, which='major', color='0.8', linestyle='-')
# axs.grid(visible=True, which='minor', color='gray', linestyle='dotted', alpha=0.2)
axs.minorticks_on()

axs.legend((T1,S1),
           ('$T$', '$S$'),
           loc='best',
           ncol=1,
           fontsize=12)
axs.text(8,0.4,
         '$\eta_2 = 1.0$',
         fontsize = 12,
         bbox = dict(boxstyle="round,pad=0.6",facecolor = 'white', alpha = 0.5,edgecolor='black'))
axs.text(6,3.1,
         '$\Psi <0$',
         fontsize = 12,
         bbox = dict(boxstyle="round,pad=0.6",facecolor = 'white', alpha = 0.5,edgecolor='None'))
axs.text(8,1.25,
         '$\Psi >0$',
         fontsize = 12,
         bbox = dict(boxstyle="round,pad=0.6",facecolor = 'white', alpha = 0.5,edgecolor='None'))
axs.text(6,0.6,
         '$\Psi >0$',
         fontsize = 12,
         bbox = dict(boxstyle="round,pad=0.6",facecolor = 'white', alpha = 0.5,edgecolor='None'))
plt.savefig('../figs/trajectory2.pdf')
###
