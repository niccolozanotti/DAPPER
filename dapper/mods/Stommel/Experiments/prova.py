import sympy as smp

import numpy as np

T = smp.Symbol('T', real = True)
S = smp.Symbol('S', real = True)
eta1 = 1.
eta2 = 2.
eta3 = 3.

sol = smp.solve([(T*(1 + np.abs(T - S) - eta1)).rewrite(smp.Piecewise),(S*(eta3 + np.abs(T - S)) - eta2).rewrite(smp.Piecewise)])

print(sol)