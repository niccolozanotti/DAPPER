import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import dapper.mods.Stommel.Experiments as exp
import os
import scienceplots
# from matplotlib.legend_handler import HandlerLine2D
rc('text', usetex=True)
plt.style.use(['science']) # style used in scientific papers(LaTeX based)

ref_forcing = np.load('Data/ref_forcing_var.npz')
ref_forcing_da = np.load('Data/ref_forcing_var_da.npz')

levels = np.arange(0., 1.1, .1)

# DA = off
fig1,ax1 = plt.subplots()
ax1.set_xlabel("$\sigma_T$ (°C)")
ax1.set_ylabel("$\sigma_S$ (ppt)")
cs1 = ax1.contourf(ref_forcing['arr_0'], ref_forcing['arr_1'], ref_forcing['arr_2'], levels)
fig1.colorbar(cs1)

fig1.text(0.45, 0.92, "DA", fontsize='large', color='r', ha ='center')
fig1.savefig(os.path.join(exp.fig_dir,
                         'ref_forcing_var.png'), format='png', dpi=500)

# DA = on
fig2,ax2 = plt.subplots()
ax2.set_xlabel("$\sigma_T$ (°C)")
ax2.set_ylabel("$\sigma_S$ (ppt)")
cs2 = ax2.contourf(ref_forcing_da['arr_0'], ref_forcing_da['arr_1'], ref_forcing_da['arr_2'], levels)
fig2.colorbar(cs2)

fig2.text(0.45, 0.92, "DA", fontsize='large', color='g', ha ='center')
fig2.savefig(os.path.join(exp.fig_dir,
                         'ref_forcing_var_da.png'), format='png', dpi=500)