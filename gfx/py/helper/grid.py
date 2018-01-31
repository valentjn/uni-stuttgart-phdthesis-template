import numpy as np
import scipy.misc

class RegularSparse(object):
  def __init__(self):
    _d = None
    _n = None
    _Xl = None
    _Xi = None
    _l = None
    _l1 = None
    _i = None
    _t = None
    _m = None
  
  def getSize(self, d, n):
    if n <= 0:
      return 1 if d == 0 else 0
    elif d == 0:
      return 1
    elif d < 0:
      return 0
    else:
      return sum([2**k * scipy.misc.comb(d-1+k, d-1, exact=True)
                  for k in range(n)])
  
  def generate(self, d, n):
    self._d = d
    self._n = n
    N = self.getSize(d, n)
    self._Xl = np.zeros((N, d))
    self._Xi = np.zeros((N, d))
    self._l = np.ones((d,))
    self._l1 = d
    self._i = np.ones((d,))
    self._t = 0
    self._m = 0
    
    self._generateRecursively()
    
    Xl = self._Xl
    Xi = self._Xi
    X = Xi * 2**(-Xl)
    
    return X, Xl, Xi
  
  def _generateRecursively(self):
    if self._t == self._d:
      self._Xl[self._m,:] = self._l
      self._Xi[self._m,:] = self._i
      self._m += 1
    elif self._l1 <= self._n + self._d - 1:
      self._l[self._t] += 1
      self._l1 += 1
      self._i[self._t] = 2 * self._i[self._t] - 1
      self._generateRecursively()
      self._i[self._t] += 2
      self._generateRecursively()
      self._l[self._t] -= 1
      self._l1 -= 1
      self._i[self._t] = (self._i[self._t] - 1) / 2
      
      self._t += 1
      self._generateRecursively()
      self._t -= 1

