#!/usr/bin/python3

import numpy as np
import scipy.misc



def getNodalIndices(l):
  i1D = [getNodalIndices1D(l1D) for l1D in l]
  meshGrid = np.meshgrid(*i1D, indexing="ij")
  I = np.column_stack([grid.flatten() for grid in meshGrid])
  return I

def getNodalIndices1D(l):
  i = list(range(2**l + 1))
  return i

def getHierarchicalIndices(l):
  i1D = [getHierarchicalIndices1D(l1D) for l1D in l]
  meshGrid = np.meshgrid(*i1D, indexing="ij")
  I = np.column_stack([grid.flatten() for grid in meshGrid])
  return I

def getHierarchicalIndices1D(l):
  i = (list(range(1, 2**l, 2)) if l > 0 else [0, 1])
  return i

def getCoordinates(L, I, distribution="uniform"):
  L, I = np.array(L), np.array(I)
  if L.size == 1: L = L * np.ones_like(I)
  
  if distribution == "uniform":
    X = I / 2**L
  elif distribution == "clenshawCurtis":
    HInv = 2**L
    K1 = (I < 0)
    K2 = (I > HInv)
    K = np.logical_not(np.logical_or(K1, K2))
    X = np.zeros(L.shape)
    X[K] = (1 - np.cos(np.pi * I[K] / HInv[K])) / 2
    X[K1] = I[K1] * ((1 - np.cos(np.pi / HInv[K1])) / 2)
    X[K2] = 1 + (I[K2] - HInv[K2]) * ((1 - np.cos(np.pi / HInv[K2])) / 2)
  else:
    raise NotImplementedError("Unknown grid point distribution.")
  
  return X

def generateMeshGrid(nns):
  assert len(nns) == 2
  xx0 = np.linspace(0, 1, nns[0])
  xx1 = np.linspace(0, 1, nns[1])
  XX0, XX1 = np.meshgrid(xx0, xx1)
  XX = flattenMeshGrid((XX0, XX1))
  return XX0, XX1, XX

def flattenMeshGrid(XXs):
  XX = np.stack([XXt.flatten() for XXt in XXs], axis=1)
  return XX



class RegularSparse(object):
  def __init__(self, n, d):
    self.n = n
    self.d = d
  
  def getSize(self):
    if self.n <= 0:
      return (1 if self.d == 0 else 0)
    elif self.d == 0:
      return 1
    elif self.d < 0:
      return 0
    else:
      return sum([2**q * scipy.misc.comb(self.d - 1 + q, self.d - 1, exact=True)
                  for q in range(self.n - self.d + 1)])
  
  def generate(self):
    n = self.n
    d = self.d
    N = self.getSize()
    L = np.zeros((N, d))
    I = np.zeros((N, d))
    l = np.ones((d,))
    l1 = d
    i = np.ones((d,))
    t = 0
    m = 0
    
    def generateRecursively():
      nonlocal n, d, L, I, l, l1, i, t, m
      
      if t == d:
        L[m,:] = l
        I[m,:] = i
        m += 1
      elif l1 <= n:
        l[t] += 1
        l1 += 1
        i[t] = 2 * i[t] - 1
        generateRecursively()
        i[t] += 2
        generateRecursively()
        l[t] -= 1
        l1 -= 1
        i[t] = (i[t] - 1) / 2
        
        t += 1
        generateRecursively()
        t -= 1
    
    generateRecursively()
    X = I * 2**(-L)
    
    return X, L, I



class RegularSparseBoundary(object):
  def __init__(self, n, d, b):
    self.n = n
    self.d = d
    self.b = b
  
  def getSize(self):
    if self.b == 0:
      return sum([2**q * scipy.misc.comb(self.d, q, exact=True) *
                  RegularSparse(self.n, self.d - q).getSize()
                  for q in range(self.d + 1)])
    elif self.b >= 1:
      return (RegularSparse(self.n, self.d).getSize() +
              sum([2**q * scipy.misc.comb(self.d, q, exact=True) *
                   RegularSparse(self.n - q - self.b + 1, self.d - q).getSize()
                   for q in range(1, self.d + 1)]))
    else:
      raise ValueError("Invalid value for b.")
  
  def generate(self):
    n, d, b = self.n, self.d, self.b
    
    if self.b == 0:
      oldL = [[l] for l in range(n+1)]
      newL = list(oldL)
      
      for t in range(2, d+1):
        newL = []
        
        for l in oldL:
          lNorm = sum(l)
          lStar = n - lNorm
          newL.extend([(*l, lt) for lt in range(0, lStar+1)])
        
        oldL = list(newL)
      
      L = np.array(newL)
    
    elif self.b >= 1:
      oldL = [[l] for l in range(n-d+2)]
      newL = list(oldL)
      
      for t in range(2, d+1):
        newL = []
        
        for l in oldL:
          lNorm = sum(l)
          Nl = sum([lt == 0 for lt in l])
          
          if (lNorm + Nl <= n - d + t - b) or (Nl == t-1):
            newL.append((*l, 0))
          
          if Nl == 0: lStar = n - d + t - lNorm
          else:       lStar = n - d + t - b + 1 - lNorm - Nl
          newL.extend([(*l, lt) for lt in range(1, lStar+1)])
        
        oldL = list(newL)
      
      L = np.array(newL)
    
    else:
      raise ValueError("Invalid value for b.")
    
    return DimensionallyAdaptiveSparse(L).generate()



class DimensionallyAdaptiveSparse(object):
  def __init__(self, L):
    self.L = L
  
  def generate(self):
    I = [getHierarchicalIndices(self.L[k,:]) for k in range(self.L.shape[0])]
    
    if len(I) > 0:
      L = np.vstack([np.tile(self.L[k,:], [I[k].shape[0], 1])
                     for k in range(self.L.shape[0])])
      I = np.vstack(I)
    else:
      L = []
    
    X = getCoordinates(L, I)
    return X, L, I



class SGppGrid(object):
  def __init__(self, grid, *args):
    if type(grid) is str:
      import pysgpp
      self.label = "{}({})".format(grid, ", ".join([str(arg) for arg in args]))
      gridTypes = {
        "bSpline" : pysgpp.Grid.createBsplineBoundaryGrid,
        "bSplineNoBoundary" : pysgpp.Grid.createBsplineGrid,
        "modifiedBSpline" : pysgpp.Grid.createModBsplineGrid,
        "modifiedNotAKnotBSpline" : pysgpp.Grid.createModNotAKnotBsplineGrid,
        "notAKnotBSpline" : pysgpp.Grid.createNotAKnotBsplineBoundaryGrid,
      }
      grid = gridTypes[grid](*args)
    
    self.grid = grid
  
  def generateRegular(self, n):
    self.grid.getStorage().clear()
    self.grid.getGenerator().regular(n)
    return self.getPoints()
  
  def getPoints(self):
    gridStorage = self.grid.getStorage()
    N = gridStorage.getSize()
    d = gridStorage.getDimension()
    L = np.zeros((N, d), dtype=np.uint64)
    I = np.zeros((N, d), dtype=np.uint64)
    
    for k in range(N):
      gp = gridStorage.getPoint(k)
      
      for t in range(d):
        L[k,t] = gp.getLevel(t)
        I[k,t] = gp.getIndex(t)
    
    X = getCoordinates(L, I)
    return X, L, I
  
  def __str__(self):
    return self.label
