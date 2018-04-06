#!/usr/bin/python3
# number of output figures = 2

import numpy as np
import scipy.optimize

import helper.basis
from helper.figure import Figure



p = 3
color = 3 * [0.6]



xl = (-30, 30)

fig = Figure.create(figsize=(6.48, 0.8))
ax = fig.gca()

basis = helper.basis.CentralizedCardinalBSpline(p, nu=0)
maxValue = basis.evaluate(0)
offset = (4 * scipy.optimize.root(
  lambda x: basis.evaluate(x) - maxValue/2, (p+1)/4).x[0])

xl = [offset * (xl[0] // offset), offset * (xl[1] // offset)]
xx = np.linspace(*xl, 1001)

for k in range(-25, 26):
  yy = 2/maxValue * basis.evaluate(xx - offset*k) - 1
  K = (yy > -1)
  ax.plot(xx[K], yy[K], "-", color=color)
  ax.plot(xx[K], -yy[K], "-", color=color)

ax.plot(xl, [-1, -1], "-", color=color)
ax.plot(xl, [1, 1], "-", color=color)

#offset = (p+1)/2
#basis = helper.basis.CentralizedCardinalBSpline(p, nu=-1)
#
#xx = np.linspace(*xl, 1001)
#yyLine = np.minimum(basis.evaluate(xx + offset),
#                    basis.evaluate(-xx + offset))
#
#K = (yyLine > 0)
#ax.plot(xx, yyLine, "-", color=color, lw=1.5)
#ax.plot(xx[K], -yyLine[K], "-", color=color, lw=1.5)
#
##ax.fill(np.hstack((xx[K], xx[K][::-1])),
##        np.hstack((-yyLine[K], yyLine[K][::-1])),
##        fc=color, ec="none")
#
#basis = helper.basis.CentralizedCardinalBSpline(p)
#
#for k in range(-2, 3):
#  yy = np.minimum(np.maximum(
#    3 * basis.evaluate(xx - 3*k) - 1, -yyLine), yyLine)
#  
#  K = np.logical_and((yy < yyLine), (yy > -yyLine))
#  ax.plot(xx[K], yy[K], "-", color=color, lw=1.5)
#  ax.plot(xx[K], -yy[K], "-", color=color, lw=1.5)
#
#"""
#ax.plot([-offset-(p+1)/2, offset+(p+1)/2], [0, 0], "-", color=color)
#
#basis = helper.basis.CentralizedCardinalBSpline(p, nu=1)
#
#for s in [-1, 1]:
#  yy = -s * np.minimum(s * basis.evaluate(
#    xx - s * (offset + (p+1)/2)), 0)
#  K = (s * yy > 0)
#  ax.plot(xx[K], yy[K], "-", color=color)
#  ax.plot(xx[K], -yy[K], "-", color=color)
#  ax.fill(np.hstack((xx[K], xx[K][::-1])),
#          np.hstack((-yy[K], yy[K][::-1])),
#          fc=color, ec="none")
#"""

ax.set_xlim(xl)
ax.set_axis_off()

fig.save()



p = 3
xl = (-3, 3)

fig = Figure.create(figsize=(2, 0.7))
ax = fig.gca()

basis = helper.basis.CentralizedCardinalBSpline(p, nu=1)

xx = np.linspace(*xl, 1001)
yy = basis.evaluate(xx)
ax.plot(xx, yy, "-", color=color)
ax.plot(xx, -yy, "-", color=color)
ax.fill(np.hstack((xx, xx[::-1])),
        np.hstack((np.maximum(yy, -yy),
                   np.minimum(yy, -yy))),
        fc=color, ec="none")

ax.set_xlim(xl)
ax.set_axis_off()

fig.save()
