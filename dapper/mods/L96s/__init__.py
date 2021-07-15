########################################################################################
########################################################################################
"""A 1D emulator of chaotic atmospheric behaviour, including additive noise.

`bib.grudzien2020numerical`
"""


########################################################################################
########################################################################################
# Imports
import numpy as np

from dapper.mods.integration import rk4

from .extras import LPs, d2x_dtdx, dstep_dx

########################################################################################
########################################################################################
# Method definitions
########################################################################################
########################################################################################
# basic Lorenz 96 defintions and functions

__pdoc__ = {"demo": False}

# energy injected into the system
Force = 8.0

# ?
Tplot = 10


def x0(M):
    return np.eye(M)[0]


def shift(x, n):
    return np.roll(x, -n, axis=-1)


def dxdt_autonomous(x):
    return (shift(x, 1)-shift(x, -2))*shift(x, -1) - x


def dxdt(x):
    return dxdt_autonomous(x) + Force


########################################################################################
# 2nd order strong taylor SDE step

def l96s_tay2_step(x, t, dt, s):
    """Steps forward state of L96s model by order 2.0 Taylor scheme

    This is the basic formulation which makes a Fourier truncation at p=1 for the simple
    form of the order 2.0 method. See `bib.grudzien2020numerical` for full details of
    the scheme and other versions."""

    # Infer system dimension
    sys_dim = len(x)

    # Compute the deterministic dxdt and the jacobian equations
    dx = dxdt(x)
    dxF = d2x_dtdx(x)

    # coefficients defined based on the p=1 Fourier truncation
    rho = 1.0/12.0 - 0.5 * np.pi**(-2)
    alpha = np.pi**2 / 180.0 - 0.5 * np.pi**(-2)

    # draw standard normal sample to define the
    # recursive Stratonovich integral coefficients
    rndm = np.random.standard_normal([5, sys_dim])
    xi = rndm[0, :]

    mu = rndm[1, :]
    phi = rndm[2, :]

    zeta = rndm[3, :]
    eta = rndm[4, :]

    # define the auxiliary functions of random Fourier coefficients, a and b
    a = -2.0 * np.sqrt(dt * rho) * mu - np.sqrt(2.0*dt) * zeta  / np.pi
    b = np.sqrt(dt * alpha) * phi + np.sqrt(dt / (2.0 * np.pi**2) ) * eta

    # vector of first order Stratonovich integrals
    J_pdelta = (dt/2.0) * (np.sqrt(dt) * xi + a)

    def Psi(l1, l2):
        # psi will be a generic function of the indicies l1 and l2, we will define
        # psi plus and psi minus via this
        psi = dt**2 * xi[l1] * xi[l2] / 3.0 + dt * a[l1] * a[l2] / 2.0 \
              + dt**(1.5) * (xi[l1] * a[l2] + xi[l2] * a[l1]) / 4.0 \
              - dt**(1.5) * (xi[l1] * b[l2] + xi[l2] * b[l1]) / (2.0 * np.pi)
        return psi

    # we define the approximations of the second order Stratonovich integral
    psi_plus = np.array([Psi((i-1) % sys_dim, (i+1) % sys_dim)
                         for i in range(sys_dim)])
    psi_minus = np.array([Psi((i-2) % sys_dim, (i-1) % sys_dim)
                         for i in range(sys_dim)])

    # the final vectorized step forward is given as
    x  = x + dx * dt + dt**2 * 0.5 * dxF @ dx  # deterministic taylor step
    x += s * np.sqrt(dt) * xi                  # stochastic euler step
    x += s * dxF @ J_pdelta                    # stochastic first order taylor step
    x += s**2 * (psi_plus - psi_minus)         # stochastic second order taylor step

    return x


########################################################################################
