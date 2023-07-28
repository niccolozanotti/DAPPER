# -*- coding: utf-8 -*-

"""
Keep T_warming constant, change final temperature in the equator and polar basin
"""
import numpy as np
import dapper.mods as modelling
import dapper.mods.Stommel as stommel
import dapper.mods.Stommel.Experiments as exp
from dapper.da_methods.ensemble import EnKF
import matplotlib.pyplot as plt
from matplotlib import rc
from scipy.interpolate import interp1d
from copy import copy
import os
import scienceplots
# from matplotlib.legend_handler import HandlerLine2D
rc('text', usetex=True)
plt.style.use(['science']) # style used in scientific papers(LaTeX based)

def exp_clima_forcing(N=100, seed=1000, T_p_f = 6.0, T_e_f= 3.0, DA = True, Melt = True):
    # Time period for DA

    Tda = 20 * stommel.year
    T_warming = 100*stommel.year
    # Timestepping. Timesteps of 1 day, running for 200 year.
    if DA == True:
        kko = np.arange(1, int(Tda / stommel.year) + 1)
    else:
        kko = np.array([])
    tseq = modelling.Chronology(stommel.year, kko=kko,
                                T=200 * stommel.year, BurnIn=0)  # 1 observation/year
    # Create model
    model = stommel.StommelModel()
    # Heat air fluxes
    functions = stommel.default_air_temp(N)
    # Add linear warming with 6C/T_warming over the pole and 3C/T_warming over the equatior.
    trend = interp1d(np.array([0., T_warming]), np.array([[0., T_p_f], [0., T_e_f]]),
                     fill_value='extrapolate', axis=1)
    trended = [stommel.add_functions(func, trend) for func in functions]
    # Add random temperature perturbations with std dev. of 2C
    noised = [stommel.add_noise(func, seed=seed + n * 20 + 1, sig=np.array([2., 2.]))
              for n, func in enumerate(trended)]
    # For time<Tda all ensemble member n uses noised[0] after that noised[n]
    functions = [stommel.merge_functions(Tda, noised[0], func)
                 for func in noised]
    # Activate surface heat flux. functions[n] contains atm. temperature for ensemble member n.
    model.fluxes.append(stommel.TempAirFlux(functions))
    # Salinity air fluxes
    functions = stommel.default_air_salt(N)
    # Add random salinity perturbations with std dev. of 0.2ppt
    noised = [stommel.add_noise(func, seed=seed + n * 20 + 2, sig=np.array([.2, .2]))
              for n, func in enumerate(functions)]
    # For time<Tda all ensemble member n uses noised[0] after that noised[n]
    functions = [stommel.merge_functions(Tda, noised[0], func)
                 for func in noised]
    # Activate surface salinity flux.
    model.fluxes.append(stommel.SaltAirFlux(functions))
    if Melt == True:
        # Melt flux
        melt_rate = -stommel.V_ice * np.array([1.0 / (model.dx[0, 0] * model.dy[0, 0]), 0.0]) / T_warming  # ms-1
        # Default evaporation-percipitation flux (=0)
        functions = stommel.default_air_ep(N)
        # Add effect Greenland melt with annual rate melt_rate
        functions = [stommel.merge_functions(T_warming, lambda t: func(t) + melt_rate, func)
                     for func in functions]
        # Activate EP flux.
        model.fluxes.append(stommel.EPFlux(functions))
    # Default initial conditions
    x0 = model.x0
    # Variance in initial conditions and parameters.
    B = stommel.State().zero()
    B.temp += 0.5 ** 2  # C2
    B.salt += 0.05 ** 2  # ppt2
    B.temp_diff += (0.3 * model.init_state.temp_diff) ** 2
    B.salt_diff += (0.3 * model.init_state.salt_diff) ** 2
    B.gamma += (0.3 * model.init_state.gamma) ** 2
    X0 = modelling.GaussRV(C=B.to_vector(), mu=x0)
    # Dynamics model. All model error is assumed to be in forcing.
    Dyn = {'M': model.M,
           'model': model.step,
           'noise': 0
           }
    # Default observations.
    Obs = model.obs_ocean()
    # Create model.
    HMM = modelling.HiddenMarkovModel(Dyn, Obs, tseq, X0)
    # Create DA
    xp = EnKF('Sqrt', N)

    return xp, HMM, model

DA = True
Melt = False
T_p_f = np.arange(0., 9., 1.)
T_e_f = np.arange(0., 4.5, .5)
grid_x, grid_y = np.meshgrid(T_p_f, T_e_f)
Z = np.zeros_like(grid_x)

for i in range(len(T_p_f)):
    for j in range(len(T_e_f)):
        xp, HMM, model = exp_clima_forcing(T_p_f= T_p_f[i], T_e_f= T_e_f[j], DA=DA, Melt=Melt)

        # Run
        xx, yy = HMM.simulate()
        Efor, Eana = xp.assimilate(HMM, xx, yy)

        Z[j,i] = stommel.prob_change(Efor)

print(grid_x)
print(grid_y)
print(Z)

fig,ax = plt.subplots()
ax.set_xlabel("pole warming rate (K/100 year)")
ax.set_ylabel("equator warming rate (K/100 year)")
levels = np.arange(0., 1.1, .1)
cs = ax.contourf(T_p_f, T_e_f, Z, levels)
fig.colorbar(cs)

# Save figuren and file
Da = ''
melt = ''
if DA == True:
    Da = '_da'
if Melt == False:
    melt = '_nomelt'

fig.savefig(os.path.join(exp.fig_dir,
                         'clima_forcing_var2' + Da + melt + '.png'), format='png', dpi=500)
nomefile = 'Data/clima_forcing_var2' + Da + melt
np.savez(nomefile, grid_x, grid_y, Z)

