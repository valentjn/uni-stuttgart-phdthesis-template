#!/usr/bin/python3
# number of output figures = 25

import multiprocessing

import matplotlib.patches
import numpy as np

import helper.basis
from helper.figure import Figure

def drawImage(imageNumber):
  fig = Figure.create(figsize=(5, 5 * aspect), scale=0.5)
  ax = fig.gca()
  
  xUnits = imageNumber * xUnitsPerImage
  if startsInXUnits[pMin] < xUnits:
    p = max([p for p in range(pMin, pMax + 1) if startsInXUnits[p] < xUnits])
  else:
    p = pMin
  xUnits -= startsInXUnits[p]
  
  for pCur in range(pMax, -1, -1):
    if pCur == p:
      xx = np.linspace(min(max(xUnits, 0), pCur + 1), pCur + 1, 200)
      color = colorLight
    else:
      xx = np.linspace(0, pCur + 1, 200)
      color = (colorDark if pCur < p else colorLight)
    b = helper.basis.CardinalBSpline(pCur)
    yy = b.evaluate(xx)
    if pCur == 0: yy[-1] = 1
    ax.plot(xx, yy, "-", color=color, clip_on=False)
  
  b = helper.basis.CardinalBSpline(p)
  xx = np.linspace(0, min(max(xUnits, 0), p + 1), 200)
  yy = b.evaluate(xx)
  ax.plot(xx, yy, "-", color=colorDark, clip_on=False)
  
  if (0 < xUnits < p + 1) and (p > 0):
    bPrev = helper.basis.CardinalBSpline(p - 1)
    xx = np.linspace(max(xUnits - 1, 0), xUnits, 1000)
    yy = bPrev.evaluate(xx)
    xxyy = np.column_stack((np.hstack((xx, xx[::-1])),
                            np.hstack((np.zeros_like(yy), yy[::-1]))))
    ax.add_patch(matplotlib.patches.Polygon(
      xxyy, ec="none", fc=colorLight, alpha=0.5, clip_on=False))
    
    x = np.array([xUnits])
    y = b.evaluate(x)
    ax.plot(x, y, "o", color=colorDark, markersize=3, clip_on=False)
  
  ax.set_xlim(*xLim)
  ax.set_ylim(*yLim)
  ax.set_aspect("equal")
  ax.set_axis_off()
  
  fig.save(graphicsNumber=imageNumber+1, crop=False,
           tightLayout={"pad" : 0, "h_pad" : 0, "w_pad" : 0})



numberOfImages = 25
pauseStartInXUnits = 0.2
pauseBetweenInXUnits = 0.2
pauseEndInXUnits = 0.2
pMin = 1
pMax = 3
colorBase = Figure.COLORS["anthrazit"]
colorDarkBrightness = 0.3
colorLightBrightness = 0.6

colorDark =  [x + colorDarkBrightness  * (1 - x) for x in colorBase]
colorLight = [x + colorLightBrightness * (1 - x) for x in colorBase]
startsInXUnits = {pMin : pauseStartInXUnits}

for p in range(pMin + 1, pMax + 1):
  startsInXUnits[p] = startsInXUnits[p - 1] + p + pauseBetweenInXUnits

lengthInXUnits = startsInXUnits[pMax] + (pMax + 1) + pauseEndInXUnits
xUnitsPerImage = lengthInXUnits / (numberOfImages - 1)

xLim = [0, pMax + 1]
yLim = [0, 1]
aspect = (yLim[1] - yLim[0]) / (xLim[1] - xLim[0])

with multiprocessing.Pool() as pool:
  pool.map(drawImage, range(numberOfImages))
