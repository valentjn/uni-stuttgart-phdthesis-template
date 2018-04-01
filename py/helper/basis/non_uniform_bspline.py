#!/usr/bin/python3

import numpy as np
import scipy.interpolate

from .parent_function import ParentFunction

class NonUniformBSpline(ParentFunction):
  def __init__(self, p, xi, k=None, nu=0):
    if k is None:
      super().__init__(nu)
      fakeXi = np.hstack([p * [xi[0]], xi, p * [xi[-1]]])
      fakeC = np.zeros((2*p+1,))
      fakeC[p] = 1
      self.bSpline = scipy.interpolate.BSpline(fakeXi, fakeC, p)
      self.support = [xi[0], xi[-1]]
    else:
      self.__init__(p, xi[k:k+p+2], nu=nu)
  
  def evaluate(self, xx):
    xx = np.array(xx).flatten().astype(float)
    K = np.logical_and(xx >= self.support[0], xx < self.support[1])
    yy = np.zeros_like(xx)
    yy[K] = self.bSpline(xx[K], nu=self.nu)
    return yy
  
  def getSupport(self):
    return self.support
