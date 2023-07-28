import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import dapper.mods.Stommel.Experiments as exp
import os
import scienceplots
# from matplotlib.legend_handler import HandlerLine2D
rc('text', usetex=True)
plt.style.use(['science']) # style used in scientific papers(LaTeX based)

#clima_forcing_var_2
clima_var2 = np.load('Data/clima_forcing_var2.npz')
clima_var2_da = np.load('Data/clima_forcing_var2_da.npz')
clima_var2_nomelt = np.load('Data/clima_forcing_var2_nomelt.npz')
clima_var2_da_nomelt = np.load('Data/clima_forcing_var2_da_nomelt.npz')

levels = np.arange(0., 1.1, .1)

fig1,ax1 = plt.subplots()
ax1.set_xlabel("polar warming rate (°C/year)")
ax1.set_ylabel("equatorial warming rate (K/year)")
cs1 = ax1.contourf(clima_var2['arr_0'], clima_var2['arr_1'], clima_var2['arr_2'], levels)
fig1.colorbar(cs1)

fig1.text(0.40, 0.92, "DA", fontsize='large', color='r', ha ='right')
fig1.text(0.45, 0.92, "Melt", fontsize='large', color='g', ha ='left')

plt.show()