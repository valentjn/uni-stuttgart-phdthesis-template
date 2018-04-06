#!/usr/bin/python3
# number of output figures = 2

import numpy as np

import helper.basis
from helper.figure import Figure



color = 3 * [0.6]



p = 3
xl = (-20, 20)
offset = (p+1)/2

fig = Figure.create(figsize=(4.5, 0.8))
ax = fig.gca()

basis = helper.basis.CentralizedCardinalBSpline(p, nu=-1)

xx = np.linspace(*xl, 1001)
yyLine = np.minimum(basis.evaluate(xx + offset),
                    basis.evaluate(-xx + offset))
ax.plot(xx, yyLine, "-", color=color)
K = (yyLine > 0)
ax.plot(xx[K], -yyLine[K], "-", color=color)

ax.fill(np.hstack((xx[K], xx[K][::-1])),
        np.hstack((-yyLine[K], yyLine[K][::-1])),
        fc=color, ec="none")

  #ax.fill(np.hstack((xx[K], xx[K][::-1])),
  #        np.hstack((np.maximum(yy[K], -yy[K]),
  #                   np.minimum(yy[K], -yy[K]))),
  #        fc=color, ec="none")

basis = helper.basis.CentralizedCardinalBSpline(p)

for k in range(-2, 3):
  yy = np.minimum(np.maximum(
    3 * basis.evaluate(xx - 4*k) - 1, -yyLine), yyLine)
  
  K = np.logical_and((yy < yyLine), (yy > -yyLine))
  ax.plot(xx[K], yy[K], "-", color=color)
  ax.plot(xx[K], -yy[K], "-", color=color)
  
  if False:
    yy = 3 * basis.evaluate(xx - 4*k) - 1
    yyLast = 3 * basis.evaluate(xx - 4*(k-1)) - 1
    print(yy)
    print(yyLast)
    yy2 = np.maximum(yyLast, yy)
    print(yy2)
    K = (yy2 < -yy2)
    print(K)
    ax.fill(np.hstack((xx[K], xx[K][::-1])),
            np.hstack((np.maximum(yy2[K], -yy2[K]),
                       np.minimum(yy2[K], -yy2[K]))),
            fc=color, ec="none")
  
  #K = (yy >= -yy)
  #ax.fill(np.hstack((xx[K], xx[K][::-1])),
  #        np.hstack((np.maximum(yy[K], -yy[K]),
  #                   np.minimum(yy[K], -yy[K]))),
  #        fc=color, ec="none")

ax.plot([-offset-(p+1)/2, offset+(p+1)/2], [0, 0], "-", color=color)

basis = helper.basis.CentralizedCardinalBSpline(p, nu=1)

for s in [-1, 1]:
  yy = -s * np.minimum(s * basis.evaluate(
    xx - s * (offset + (p+1)/2)), 0)
  K = (s * yy > 0)
  ax.plot(xx[K], yy[K], "-", color=color)
  ax.plot(xx[K], -yy[K], "-", color=color)
  ax.fill(np.hstack((xx[K], xx[K][::-1])),
          np.hstack((-yy[K], yy[K][::-1])),
          fc=color, ec="none")

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
