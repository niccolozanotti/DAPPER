#Try with different value to the variations of the starting values, and see how many members flips

import numpy as np
import dapper.mods as modelling
import dapper.mods.Stommel as stommel
from dapper.da_methods.ensemble import EnKF
import matplotlib.pyplot as plt
from copy import copy
import os

# Number of ensemble members
N = 100
# Timestepping. Timesteps of 1 day, running for 200 year.
kko = np.array([])
tseq = modelling.Chronology(stommel.year, kko=kko,
                            T=200*stommel.year, BurnIn=0)  # 1 observation/year
# Create default Stommel model
model = stommel.StommelModel()
#Switch on heat exchange with atmosphere. Assume stationary air temperatures.
model.fluxes.append(stommel.TempAirFlux(stommel.default_air_temp(N)))
#Switch on salinity exchange with atmosphere. Assume stationary air salinity.
model.fluxes.append(stommel.SaltAirFlux(stommel.default_air_salt(N)))
#Use default initial conditions.
default_init = model.init_state
# Initial conditions
x0 = model.init_state.to_vector()
# Dynamich model. All model error is assumed to be in forcing.
Dyn = {'M': model.M,
       'model': model.step,
       'noise': 0
       }
# Default observations.
Obs = model.obs_ocean()

xp = EnKF("Sqrt",N)
#Arrays for values of the variance to graph
T_min, T_max, T_step = 0.7, 1., 0.1
S_min, S_max, S_step = 0.07, 0.10, 0.01
T_var = np.arange(T_min, T_max + T_step, T_step)
S_var = np.arange(S_min, S_max + S_step, S_step)
grid_x,  grid_y = np.meshgrid(T_var,S_var)
#For the graph we want an array with coordinates (x,y,z) = (Ocean Temp Variance, ocean salinity variance,
#percentage of Ensemble that flips)
Z = np.zeros_like(grid_x)
#Try with different values for variations
for i in range(len(T_var)):
    for j in range(len(S_var)):
        #Variance Ocean temp[2], ocean salinity[2], temp diffusion parameter,
        #salt diffusion parameter, transport parameter
        B = stommel.State().zero()
        B.temp += T_var[i]**2 #C2
        B.salt += S_var[j]**2 #ppt2
        X0 = modelling.GaussRV(C=B.to_vector(), mu=x0)

        # Create model.
        HMM = modelling.HiddenMarkovModel(Dyn, Obs, tseq, X0)

        #Evaluate truth values
        xx,yy=HMM.simulate()
        #Apply DA()
        Efor, Eana = xp.assimilate(HMM, xx, yy)
        #Add points to the array to graph:
        Z[i,j] = stommel.prob_change(Efor) #o [j][i], devo ragionarci


#We now want to graph points in a 3D graph
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
ax.plot_surface(grid_x, grid_y, Z)

fig.savefig(os.path.join(stommel.fig_dir,'ref_init_var.png'),format='png',dpi=500)