#!/usr/bin/python3

import helper.grid

from .centralized_cardinal_bspline import CentralizedCardinalBSpline
from .hierarchical_basis_from_parent_function import HierarchicalBasisFromParentFunction

def restrictKnots(p, hInv, i, I):
  offset = 0
  
  if i < 0:
    I = [I[0] - j * (I[1] - I[0]) for j in range(-i, 0, -1)] + I
    offset = -i
  elif i > hInv:
    I = I + [I[-1] + j * (I[-1] - I[-2]) for j in range(1, i-hInv+1)]
  
  I = I[i+offset:i+offset+p+2]
  return I

class HierarchicalBSpline(HierarchicalBasisFromParentFunction):
  def __init__(self, p, nu=0):
    super().__init__(CentralizedCardinalBSpline(p, nu=nu))
    self.p = p
  
  def getKnots(self, l, i=None):
    hInv = 2**l
    I = list(range(-(self.p+1)//2, hInv + (self.p+1)//2 + 1))
    if i is not None: I = restrictKnots(self.p, hInv, i, I)
    xi = helper.grid.getCoordinates(l, I)
    return xi
