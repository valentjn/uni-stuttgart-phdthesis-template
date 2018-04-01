import hashlib
import lzma
import os
import pathlib
import pickle
import platform
import subprocess
import sys

import cycler
import matplotlib as mpl
import matplotlib.pyplot as plt
plt.switch_backend("pgf")
from mpl_toolkits.mplot3d import Axes3D



class Figure(mpl.figure.Figure):
  COLORS = {
    "anthrazit" :  ( 62/255,  68/255,  76/255),
    "mittelblau" : (  0/255,  81/255, 158/255),
    "hellblau"   : (  0/255, 190/255, 255/255),
  }

  _TEX_PREAMBLE_COMMON = r"""
\usepackage[ngerman,american]{babel}
\usepackage{mathtools}
\usepackage[utf8]{luainputenc}
\usepackage[T1]{fontenc}

\usepackage{xcolor}

\definecolor{anthrazit}{RGB}{62,68,76}
\definecolor{mittelblau}{RGB}{0,81,158}
\definecolor{hellblau}{RGB}{0,190,255}

\definecolor{C0}{rgb}{0.000,0.447,0.741}
\definecolor{C1}{rgb}{0.850,0.325,0.098}
\definecolor{C2}{rgb}{0.929,0.694,0.125}
\definecolor{C3}{rgb}{0.494,0.184,0.556}
\definecolor{C4}{rgb}{0.466,0.674,0.188}
\definecolor{C5}{rgb}{0.301,0.745,0.933}
\definecolor{C6}{rgb}{0.635,0.078,0.184}
\definecolor{C7}{rgb}{0.887,0.465,0.758}
\definecolor{C8}{rgb}{0.496,0.496,0.496}

% prevent Matplotlib from loading fontspec as this resets the default text font
% (the default math font will be alright with the no-math option to fontspec,
% but the text font will still be CM...)
\makeatletter
\@namedef{ver@fontspec.sty}{}
\makeatother

%\PassOptionsToPackage{no-math}{fontspec}
"""
  
  _TEX_PREAMBLE_SPECIAL = {
    "beamer" : r"""
\usepackage[scaled]{helvet}
\renewcommand*{\familydefault}{\sfdefault}
\usepackage{sfmath}
""",
    "paper" : "",
    "thesis" : r"""
\usepackage[bitstream-charter]{mathdesign}
\renewcommand*{\vec}[1]{{\boldsymbol{#1}}}
\renewcommand*{\*}[1]{\vec{#1}}
""",
  }
  
  _LINE_COLORS = [
    (0.000, 0.447, 0.741),
    (0.850, 0.325, 0.098),
    (0.929, 0.694, 0.125),
    (0.494, 0.184, 0.556),
    (0.466, 0.674, 0.188),
    (0.301, 0.745, 0.933),
    (0.635, 0.078, 0.184),
    (0.887, 0.465, 0.758),
    (0.496, 0.496, 0.496),
  ]
  
  graphicsCounter = 0
  
  def __init__(self, *args, fontSize=11, preamble="", mode=None, **kwargs):
    super(Figure, self).__init__(*args, **kwargs)
    
    if mode is None:
      if "talk" in Figure._getBuildDir():
        self.mode = "beamer"
      elif "thesis" in Figure._getBuildDir():
        self.mode = "thesis"
      else:
        self.mode = "paper"
    else:
      self.mode = mode
    
    fontFamily = ("sans-serif" if self.mode == "beamer" else "serif")
    preamble = (Figure._TEX_PREAMBLE_COMMON +
                Figure._TEX_PREAMBLE_SPECIAL[self.mode] +
                preamble)
    
    mpl.rcParams.update({
      "axes.prop_cycle" : cycler.cycler(color=Figure._LINE_COLORS),
      "font.family" : fontFamily,
      "font.size" : fontSize,
      "lines.linewidth" : 1,
      "pgf.texsystem" : "lualatex",
      "pgf.rcfonts" : False,
      "pgf.preamble" : preamble.splitlines(),
      "text.usetex" : True,
    })
    
    self._saveDisabled = (platform.node() == "neon")
  
  @staticmethod
  def create(*args, scale=1, **kwargs):
    if "figsize" in kwargs: kwargs["figsize"] = [scale * x for x in kwargs["figsize"]]
    return plt.figure(*args, FigureClass=Figure, **kwargs)
  
  @staticmethod
  def _getBuildDir():
    return os.path.realpath(os.environ["BUILD_DIR"])
  
  @staticmethod
  def _getGraphicsBasename():
    return os.path.splitext(os.path.split(os.path.realpath(sys.argv[0]))[1])[0]
  
  @staticmethod
  def _computeHash(path):
    try:
      with open(path, "rb") as f: return hashlib.md5(f.read()).digest()
    except:
      return None
  
  @staticmethod
  def load(datPath=None):
    Figure.graphicsCounter += 1
    graphicsNumber = Figure.graphicsCounter
    
    if path is None:
      buildDir = Figure._getBuildDir()
      graphicsBasename = Figure._getGraphicsBasename()
      basename = os.path.join(buildDir, "{}_{}".format(graphicsBasename, graphicsNumber))
      datPath = "{}.pickle.dat".format(basename)
    
    print("Loading {}...".format(datPath))
    with lzma.open(datPath, "rb") as f: return pickle.load(f)
  
  def disableSave():
    self._saveDisabled = True
  
  def enableSave():
    self._saveDisabled = False
  
  def save(self, graphicsNumber=None, appendGraphicsNumber=True,
           hideSpines=True, tightLayout=True, crop=True, close=True,
           transparent=True):
    plt.figure(self.number)
    
    if graphicsNumber is None:
      Figure.graphicsCounter += 1
      graphicsNumber = Figure.graphicsCounter
    else:
      Figure.graphicsCounter = graphicsNumber
    
    if self._saveDisabled:
      if close: plt.close(self)
      return
    
    if tightLayout is not False:
      if tightLayout is True: tightLayout = {}
      self.tight_layout(**tightLayout)
    
    if hideSpines:
      for ax in self.axes:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    
    if graphicsNumber is None: graphicsNumber = self.number
    
    buildDir = Figure._getBuildDir()
    graphicsBasename = Figure._getGraphicsBasename()
    
    basename = graphicsBasename
    if appendGraphicsNumber: basename += "_{}".format(graphicsNumber)
    basename = os.path.join(buildDir, basename)
    
    if transparent:
      savefigFcn = (
        lambda path: plt.savefig(path, facecolor="none", transparent=True))
    else:
      savefigFcn = (
        lambda path: plt.savefig(path, facecolor=self.get_facecolor()))
    
    pgfPath = "{}.pgf".format(basename)
    print("Saving {}...".format(os.path.split(pgfPath)[1]))
    savefigFcn(pgfPath)
    
    pgfXzPath = "{}.pgf.xz".format(basename)
    oldHash = Figure._computeHash(pgfXzPath)
    with open(pgfPath, "rb") as f: pgf = f.read()
    with lzma.open(pgfXzPath, "wb") as f: pickle.dump(pgf, f)
    os.remove(pgfPath)
    newHash = Figure._computeHash(pgfXzPath)
    
    pdfPath = "{}.pdf".format(basename)
    
    if (oldHash == newHash) and os.path.isfile(pdfPath):
      print("No changes since last run.")
      pathlib.Path(pdfPath).touch()
    else:
      print("Compiling to {}...".format(os.path.split(pdfPath)[1]))
      savefigFcn(pdfPath)
      if crop: subprocess.run(["pdfcrop", pdfPath, pdfPath], check=True)
      
      datPath = "{}.pickle.xz".format(basename)
      print("Saving {}...".format(os.path.split(datPath)[1]))
      with lzma.open(datPath, "wb") as f: pickle.dump(self, f)
    
    if close: plt.close(self)
