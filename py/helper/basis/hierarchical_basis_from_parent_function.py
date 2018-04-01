#!/usr/bin/python3

from .hierarchical_basis import HierarchicalBasis

class HierarchicalBasisFromParentFunction(HierarchicalBasis):
  def __init__(self, parentFunction):
    super().__init__(nu=parentFunction.nu)
    self.parentFunction = parentFunction
  
  def evaluate(self, l, i, xx):
    tt = 2**l * xx - i
    yy = self.parentFunction.evaluate(tt)
    yy *= 2**(l*self.nu)
    return yy
  
  def getSupport(self, l, i):
    lb, ub = self.parentFunction.getSupport()
    lb = max((lb + i) / 2**l, 0)
    ub = min((ub + i) / 2**l, 1)
    return lb, ub
