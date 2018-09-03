#!/usr/bin/python3

import argparse
import os
import re

codeHeader = r"""\glossarysection[\glossarytoctitle]{\glossarytitle}\glossarypreamble
\begin{theglossary}\glossaryheader"""
codeFooter = r"""
\end{theglossary}\glossarypostamble
"""
codeHeading = r"""{}
\glsgroupheading{{{}}}\relax \glsresetentrylist """
codeEntry = r"""%
\glossentry{{{}}}{{\glossaryentrynumbers{{\relax 
                \setentrycounter[]{{page}}\glsnumberformat{{{}}}}}}}"""


def readInput(inputPath):
  if not os.path.isfile(inputPath):
    inputPath += ".glo"
    if not os.path.isfile(inputPath):
      raise FileNotFoundError("Cannot find input path.")
  
  with open(inputPath, "r") as f: inputCode = f.read()
  return inputCode

def processInput(inputCode):
  entries = {}
  
  for line in inputCode.splitlines():
    m = re.search(r"\\glossentry\{(.*)\}\|.*\{([0-9]+)\}", line)
    key, page = m.group(1), int(m.group(2))
    key = key.replace("\"", "")
    if key not in entries: entries[key] = []
    entries[key].append(page)
  
  entries = [(x.lower(), x, y) for x, y in entries.items()]
  entries.sort()
  
  outputCode = codeHeader
  lastHeading = None
  
  for entry in entries:
    curHeading = entry[0][0].upper()
    
    if curHeading != lastHeading:
      outputCode += codeHeading.format(
        (r"\glsgroupskip" if lastHeading is not None else ""),
        curHeading)
      lastHeading = curHeading
    
    outputCode += codeEntry.format(entry[1], entry[2][0])
  
  outputCode += codeFooter
  return outputCode

def writeOutput(outputPath, outputCode):
  with open(outputPath, "w") as f: f.write(outputCode)

def main():
  parser = argparse.ArgumentParser(
                      description="Customized replacement for makeindex.")
  parser.add_argument("-q", action="store_true",
                      help="quiet mode (ignored for compatibility)")
  parser.add_argument("-o", dest="outputPath", metavar="FILENAME",
                      help="output file (usually ending with .gls)")
  parser.add_argument("inputPath", metavar="FILENAME",
                      help="input file (.glo will be appended if not found)")
  args = parser.parse_args()
  
  inputCode = readInput(args.inputPath)
  outputCode = processInput(inputCode)
  writeOutput(args.outputPath, outputCode)



if __name__ == "__main__": main()
