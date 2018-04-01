#!/usr/bin/python3

import os

capitalizationList = [
  "BSpline",
  "ClenshawCurtis",
  "NotAKnot",
  "SGpp",
]

capitalizationListLower = [word.lower() for word in capitalizationList]
dirName = os.path.dirname(__file__)

for f in os.listdir(dirName):
  if (os.path.isfile(os.path.join(dirName, f)) and
      (f.endswith(".py")) and (f != "__init__.py")):
    moduleName = f[:-3]
    words = moduleName.split("_")
    words = [word.title() for word in words]
    words = [(word if word.lower() not in capitalizationListLower else
              capitalizationList[capitalizationListLower.index(word.lower())])
             for word in words]
    className = "".join(words)
    result = __import__(moduleName, globals=globals(), locals=locals(),
                        fromlist=[className], level=1)
    vars()[className] = getattr(result, className)
