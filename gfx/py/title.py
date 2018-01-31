#!/usr/bin/python3
# number of output figures = 1

import base64
import gzip

import numpy as np

import helper.basis
from   helper.figure import Figure
import helper.grid

d = 2
n = 3
p = 3
l = (1, 1)
i = (1, 1)

b = helper.basis.HierarchicalBSpline(p)
grid = helper.grid.RegularSparse()



fig = Figure.create()
ax = fig.add_subplot(111, projection="3d")



X, Xl, Xi = grid.generate(d, n)
N = X.shape[0]
Y = np.zeros((N,))

for k in range(N):
  x = X[k,:]
  Y[k] = np.prod([b.evaluate(l[t], i[t], X[k,t]) for t in range(d)])



xx1 = np.linspace(0, 1, 129)
xx2 = np.linspace(0, 1, 129)
XX1, XX2 = np.meshgrid(xx1, xx2)
XX = np.stack((XX1.flatten(), XX2.flatten()), axis=1)
NN = XX.shape[0]
YY = np.zeros((NN,))

for k in range(NN):
  YY[k] = np.prod([b.evaluate(l[t], i[t], XX[k,t]) for t in range(d)])

YY = np.reshape(YY, XX1.shape)

color1 = "k"
color2 = Figure.COLORS["anthrazit"]
text_color = (0.04, 0.04, 0.04)
text_size = 0.4

z = 0
ax.plot_surface(XX1, XX2, np.zeros_like(XX1),
                rstride=16, cstride=16, alpha=0, edgecolors=color2)
ax.plot(X[:,0], X[:,1], zs=z, marker="o", ls="", c=color2, zorder=-1)

ax.plot_surface(XX1, XX2, YY, rstride=16, cstride=16, alpha=0, edgecolors=color1)
ax.plot(X[:,0], X[:,1], zs=Y, marker="o", ls="", c=color1)

ax.autoscale(tight=True)
ax.set_axis_off()

fig.save()
