import numpy as np
import scipy.interpolate
import scipy.signal

def coordToMotherFcn(l, i, xx):
  return 2**l * xx - i

class CardinalBSpline(object):
  def __init__(self, p):
    self.p = p
  
  def evaluate(self, xx):
    return scipy.signal.bspline(xx - (self.p+1)/2, self.p)

class HierarchicalBSpline(object):
  def __init__(self, p):
    self.p = p
    self.cardinalBSpline = CardinalBSpline(p)
  
  def evaluate(self, l, i, xx):
    t = coordToMotherFcn(l, i, xx)
    return self.cardinalBSpline.evaluate(t + (self.p+1)/2)
