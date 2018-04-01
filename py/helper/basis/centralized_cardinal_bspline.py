#!/usr/bin/python3

import numpy as np

from .non_uniform_bspline import NonUniformBSpline

class CentralizedCardinalBSpline(NonUniformBSpline):
  def __init__(self, p, nu=0):
    super().__init__(p, np.linspace(-(p+1)/2, (p+1)/2, p+2), nu=nu)
