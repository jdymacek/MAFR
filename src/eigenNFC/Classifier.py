import sys
import math

#base class for classifiers, will be overwritten by subclasses
class Classifier:
  def __init__(self, classes):
    self.classes = classes
    self.acccuracy = 0.0
    self.confusion = {k:{k:0 for k in self.classes} for k in self.classes}
  
  def classify(self, file):
    print("ERROR: MUST BE OVERWRITTEN BY SUBCLASS")
    sys.exit(1)

  def printConfusion(self):
    for k in self.confusion.keys():
      print(f"{k}",end="\t")
      for sp in self.classes:
        print(f"{self.confusion[k][sp]}",end='\t')
      print("")

  def findPecision(onlyClasses=None):
    return 0

  def findRecall(onlyClasses=None):
    return 0


  #correct label is directory
  def classifyAll(self, files):
    self.confusion = {k:{k:0 for k in self.classes} for k in self.classes}
    

    for f in files:
      result = self.classify(f)
      predicted = result.split("/")[0]
      expected = f.split("/")[-2]
      self.confusion[expected][predicted] += 1

    self.accuracy = sum([self.confusion[k][k] for k in self.classes]) / len(files)
    return self.accuracy

