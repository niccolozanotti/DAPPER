#Use the same value for starting condition but vary std deviation of the white noise(vary the magnitude)

import numpy as np
import dapper.mods as modelling
import dapper.mods.Stommel as stommel
from dapper.da_methods.ensemble import EnKF
import matplotlib.pyplot as plt
from copy import copy
import os

# Number of ensemble members
N = 100
seed=10000
Tda = 20*stommel.year
# Timestepping. Timesteps of 1 day, running for 200 year.
kko = np.array([])
tseq = modelling.Chronology(stommel.year, kko=kko,
                            T=200*stommel.year, BurnIn=0)  # 1 observation/year
#Variance Ocean temp[2], ocean salinity[2], temp diffusion parameter,
#salt diffusion parameter, transport parameter
# Dynamich model. All model error is assumed to be in forcing.


#Arrays for values of the final temperatures of pole and equator at the end of climate change
T_dev_min, T_dev_max, T_dev_step = 1.5, 4.5, 0.5
S_dev_min, S_dev_max, S_dev_step = 1.5, 4.5, 0.5
T_dev = np.arange(T_dev_min, T_dev_max + T_dev_step, T_dev_step)
S_dev = np.arange(S_dev_min, S_dev_max + S_dev_step, S_dev_step)
grid_x,  grid_y = np.meshgrid(T_dev, S_dev)
print(grid_x)
print(grid_y)
#For the graph we want an array with coordinates (x,y,z) = (Ocean Temp Variance, ocean salinity variance,
#percentage of Ensemble that flips)
Z = np.zeros_like(grid_x)
print(Z)
#Try with different values for variations
for i in range(len(T_dev)):
    for j in range(len(S_dev)):
        model = stommel.StommelModel()
        # Use default initial conditions.
        default_init = model.init_state
        # Initial conditions
        x0 = model.init_state.to_vector()
        # Switch on heat exchange with atmosphere.
        # Start with default stationary atm. temperature.
        functions = stommel.default_air_temp(N)
        # Add white noise with std dev of 2C over both pole and equator basin separately.
        noised = [stommel.add_noise(func, seed=seed + n * 20 + 1, sig=np.array(T_dev[i], T_dev[i]))
                  for n, func in enumerate(functions)]
        functions = [stommel.merge_functions(Tda, noised[0], func2)
                     for func2 in noised]
        # Switch on the atm. heat fluxes.
        model.fluxes.append(stommel.TempAirFlux(functions))
        # Salinity air fluxes
        functions = stommel.default_air_salt(N)
        # Add white with std dev. of .2 ppt.
        noised = [stommel.add_noise(func, seed=seed + n * 20 + 2, sig=np.array(T_dev[i], T_dev[i]))
                  for n, func in enumerate(functions)]
        functions = [stommel.merge_functions(Tda, noised[0], func2)
                     for func2 in noised]
        # Switch on salinity fluxes.
        model.fluxes.append(stommel.SaltAirFlux(functions))

        # Variance Ocean temp[2], ocean salinity[2], temp diffusion parameter,
        # salt diffusion parameter, transport parameter
        B = stommel.State().zero()
        B.temp += 0.5 ** 2  # C2
        B.salt += 0.05 ** 2  # ppt2
        B.temp_diff += (0.3 * model.init_state.temp_diff) ** 2
        B.salt_diff += (0.3 * model.init_state.salt_diff) ** 2
        B.gamma += (0.3 * model.init_state.gamma) ** 2
        X0 = modelling.GaussRV(C=B.to_vector(), mu=x0)

        # Dynamich model. All model error is assumed to be in forcing.
        Dyn = {'M': model.M,
               'model': model.step,
               'noise': 0
               }
        # Default observations.
        Obs = model.obs_ocean()

        # Create model.
        HMM = modelling.HiddenMarkovModel(Dyn, Obs, tseq, X0)
        xp = EnKF("Sqrt", N)
        #Evaluate truth values
        xx,yy=HMM.simulate()
        #Apply DA()
        Efor, Eana = xp.assimilate(HMM, xx, yy)
        #Add points to the array to graph:
        Z[i,j] = stommel.prob_change(Efor) #o [j][i], devo ragionarci


#We now want to graph points in a 3D graph
print(Z)
fig1, ax1 = plt.subplots(subplot_kw={"projection": "3d"})
ax1.plot_surface(grid_x, grid_y, Z)

fig1.savefig(os.path.join(stommel.fig_dir,'ref_forcing_var_3D.png'),format='png',dpi=500)

fig2, ax2 = plt.subplots()

ax2.set_xlabel("T_dev")
ax2.set_ylabel("S_dev")
ax2.contourf(grid_x, grid_y, Z)

fig2.savefig(os.path.join(stommel.fig_dir,'ref_forcing_var_col.png'),format='png',dpi=500)
