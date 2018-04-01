#!/usr/bin/python3

from .non_uniform_bspline import NonUniformBSpline

class CardinalBSpline(NonUniformBSpline):
  def __init__(self, p, nu=0):
    super().__init__(p, list(range(0, p+2)), nu=nu)
