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

# DA = off, Melt = on
fig1,ax1 = plt.subplots()
ax1.set_xlabel("polar warming rate (°C/year)")
ax1.set_ylabel("equatorial warming rate (°C/year)")
cs1 = ax1.contourf(clima_var2['arr_0']/100, clima_var2['arr_1']/100, clima_var2['arr_2'], levels)
fig1.colorbar(cs1)

fig1.text(0.40, 0.92, "DA", fontsize='large', color='r', ha ='right')
fig1.text(0.45, 0.92, "Melt", fontsize='large', color='g', ha ='left')
fig1.savefig(os.path.join(exp.fig_dir,
                         'clima_forcing_var2.png'), format='png', dpi=500)

# DA = on, Melt = on
fig2,ax2 = plt.subplots()
ax2.set_xlabel("polar warming rate (°C/year)")
ax2.set_ylabel("equatorial warming rate (°C/year)")
cs2 = ax2.contourf(clima_var2_da['arr_0']/100, clima_var2_da['arr_1']/100, clima_var2_da['arr_2'], levels)
fig2.colorbar(cs2)

fig2.text(0.40, 0.92, "DA", fontsize='large', color='g', ha ='right')
fig2.text(0.45, 0.92, "Melt", fontsize='large', color='g', ha ='left')
fig2.savefig(os.path.join(exp.fig_dir,
                         'clima_forcing_var2_da.png'), format='png', dpi=500)

# DA = off, Melt = off
fig3,ax3 = plt.subplots()
ax3.set_xlabel("polar warming rate (°C/year)")
ax3.set_ylabel("equatorial warming rate (°C/year)")
cs3 = ax3.contourf(clima_var2_nomelt['arr_0']/100, clima_var2_nomelt['arr_1']/100, clima_var2_nomelt['arr_2'], levels)
fig3.colorbar(cs3)

fig3.text(0.40, 0.92, "DA", fontsize='large', color='r', ha ='right')
fig3.text(0.45, 0.92, "Melt", fontsize='large', color='r', ha ='left')
fig3.savefig(os.path.join(exp.fig_dir,
                         'clima_forcing_var2_nomelt.png'), format='png', dpi=500)

# DA = on, Melt = off
fig4,ax4 = plt.subplots()
ax4.set_xlabel("polar warming rate (°C/year)")
ax4.set_ylabel("equatorial warming rate (°C/year)")
cs4 = ax4.contourf(clima_var2_da_nomelt['arr_0']/100, clima_var2_da_nomelt['arr_1']/100, clima_var2_da_nomelt['arr_2'], levels)
fig4.colorbar(cs4)

fig4.text(0.40, 0.92, "DA", fontsize='large', color='g', ha ='right')
fig4.text(0.45, 0.92, "Melt", fontsize='large', color='r', ha ='left')
fig4.savefig(os.path.join(exp.fig_dir,
                         'clima_forcing_var2_da_nomelt.png'), format='png', dpi=500)

plt.show()