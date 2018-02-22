#!/usr/bin/python3
# number of output figures = 1

import numpy as np

import helper.basis
from helper.figure import Figure

p = 2
k_min = 1
k_max = 3

fig = Figure.create(figsize=(5, 5), scale=0.2)
ax = fig.gca()
basis = helper.basis.CardinalBSpline(p)

for k in range(k_min, k_max + 1):
  xx = np.linspace(k, k + p + 1, 1000)
  yy = basis.evaluate(xx - k)
  ax.plot(xx, yy, color=3*[0.5], linewidth=3)

ax.set_axis_off()
ax.set_xlim(p + 1, p + 2)
ax.set_ylim(-0.03, max(yy) + 0.03)
ax.set_position([0, 0, 1, 1])

fig.save(appendGraphicsNumber=False, tightLayout=False, crop=False)
