#!/usr/bin/python3

import abc

class HierarchicalBasis(abc.ABC):
  def __init__(self, nu=0):
    self.nu = nu
  
  @abc.abstractmethod
  def evaluate(self, l, i, xx): pass

  @abc.abstractmethod
  def getSupport(self, l, i): pass
