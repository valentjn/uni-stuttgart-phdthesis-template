#!/usr/bin/python3

import abc

class ParentFunction(abc.ABC):
  def __init__(self, nu=0):
    self.nu = nu
  
  @abc.abstractmethod
  def evaluate(self, xx): pass

  @abc.abstractmethod
  def getSupport(self): pass
