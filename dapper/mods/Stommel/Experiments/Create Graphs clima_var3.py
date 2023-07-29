import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import dapper.mods.Stommel.Experiments as exp
import os
import scienceplots
# from matplotlib.legend_handler import HandlerLine2D
rc('text', usetex=True)
plt.style.use(['science']) # style used in scientific papers(LaTeX based)

#clima_var3_10 = np.load('Data/clima_forcing_var3_10.0%.npz')
clima_var3_da_10 = np.load('Data/clima_forcing_var3_da_10.0%.npz')
#clima_var3_50 = np.load('Data/clima_forcing_var3_50.0%.npz')
clima_var3_da_50 = np.load('Data/clima_forcing_var3_da_50.0%.npz')
#clima_var3_90 = np.load('Data/clima_forcing_var3_90.0%.npz')
clima_var3_da_90 = np.load('Data/clima_forcing_var3_da_90.0%.npz')

# 10%
fig1,ax1 = plt.subplots()
ax1.set_xlabel("polar warming rate (°C/year)")
ax1.set_ylabel("Melt time (Years)")
ax1.scatter(clima_var3_da_10['arr_0']/100, clima_var3_da_10['arr_1'], marker = ".")

fig1.text(0.5, 0.9, "10\%", fontsize='large', ha ='center')
fig1.savefig(os.path.join(exp.fig_dir,
                         'clima_forcing_var3_da_10.0%.png'), format='png', dpi=500)

# 50%
fig2,ax2 = plt.subplots()
ax2.set_xlabel("polar warming rate (°C/year)")
ax2.set_ylabel("Melt time (Years)")
ax2.scatter(clima_var3_da_50['arr_0']/100, clima_var3_da_50['arr_1'], marker = ".")

fig2.text(0.5, 0.9, "50\%", fontsize='large', ha ='center')
fig2.savefig(os.path.join(exp.fig_dir,
                         'clima_forcing_var3_da_50.0%.png'), format='png', dpi=500)

# 90%
fig3,ax3 = plt.subplots()
ax3.set_xlabel("polar warming rate (°C/year)")
ax3.set_ylabel("Melt time (Years)")
ax3.scatter(clima_var3_da_90['arr_0']/100, clima_var3_da_90['arr_1'], marker = ".")

fig3.text(0.5, 0.9, "90\%", fontsize='large', ha ='center')
fig3.savefig(os.path.join(exp.fig_dir,
                         'clima_forcing_var3_da_90.0%.png'), format='png', dpi=500)