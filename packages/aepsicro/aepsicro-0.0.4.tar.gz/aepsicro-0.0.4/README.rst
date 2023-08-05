A python library to perform psychrometrics analysis

Calculations are made by implementing equations described in 2009 ASHRAE Handbook—Fundamentals (SI).

There are three main classes to use this package: AIRE_HUMEDO, FLUJO, PSICROMETRICO.

AIRE_HUMEDO represents a psychrometric state.
FLUJO represents a stream in a particular state.
PSICROMETRICO shows a psychrometric diagram in a window that allows to plot states

Install:
pip install aepsicro

Usage:

from aepsicro import aepsicro as ps
s1 = ps.AIRE_HUMEDO(tseca=20, humrel=(0.5, '%1'))
s2 = ps.AIRE_HUMEDO(tseca=(30,'ºC'), humrel=(0.9, '%1'))
print(s1)
print(s2)
f1 = ps.FLUJO(s1,(1000, 'm3/h'))
f2 = ps.FLUJO(s2,(500, 'm3/h'))
# Adiabatic mixture
f3 = f1 + f2
psi = ps.PSICROMETRICO()
psi.marca_proceso(f1, f2, f3)
