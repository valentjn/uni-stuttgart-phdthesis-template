#!/usr/bin/python3
# number of output figures = 2

import numpy as np
import scipy.optimize

import helper.basis
from helper.figure import Figure



p = 3
color = 3 * [0.6]
yl = [-0.77, 0.77]

for figsize, xl in [((4.42, 0.71), (-9, 9)), ((2, 0.71), (-3, 3))]:
  fig = Figure.create(figsize=figsize)
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
  ax.set_ylim(yl)
  ax.set_axis_off()
  
  fig.save()
