from Classifier import Classifier
import MAFR
from sklearn import decomposition
import numpy as np
import csv
import eigenNFC
import sys
from collections import Counter

class EigenClassifier(Classifier):
  def updateModel(self, patterns, weights):
    self.weights = weights
    self.patterns = patterns
    self.model.components_ = patterns

  def __init__(self, classes, numPatterns, width, height):
    super(EigenClassifier, self).__init__(classes)

    self.patterns = None
    self.weights = None
    self.width = width
    self.height = height
  
    self.model = decomposition.NMF(n_components=numPatterns, init="random", random_state=0, solver="mu", max_iter=10000)
    
    M = [np.ones(self.width*self.height)]
    self.model.fit(M)
    
  def classify(self, file):
    M1 = [[eigenNFC.imageToVector(file, x=(256-self.width)//2, y=0, width=self.width, height=self.height)]]
    M = np.concatenate(M1)
    W = self.model.transform(M)

    best = ("JUNK", 9999)
    for w in self.weights:
      arr = np.array(w[1], dtype=np.float32)
      guess = w[0].split("/")[0]
      error = np.linalg.norm(arr - W[0])
      if error < best[1]:
        best = (guess, error)

    return best[0]

class EigenMajority(Classifier):
  def updateModel(self, patterns, weights):
    self.weights = weights
    self.patterns = patterns
    self.model.components_ = patterns

  def __init__(self, classes, numPatterns, width, height):
    super(EigenMajority, self).__init__(classes)

    self.patterns = None
    self.weights = None
    self.width = width
    self.height = height
  
    self.model = decomposition.NMF(n_components=numPatterns, init="random", random_state=0, solver="mu", max_iter=10000)
    
    M = [np.ones(self.width*self.height)]
    self.model.fit(M)
    
  def classify(self, file):
    M1 = [[eigenNFC.imageToVector(file, x=(256-self.width)//2, y=0, width=self.width, height=self.height)]]
    M = np.concatenate(M1)
    W = self.model.transform(M)

    errors = []
    best = ("JUNK", 9999)
    for w in self.weights:
      arr = np.array(w[1], dtype=np.float32)
#guess = w[0]
      guess = w[0].split("/")[0]
      error = np.linalg.norm(arr - W[0])
      e = (error, guess)
      errors.append(e)
      if error < best[1]:
        best = (guess, error)

    topFive = sorted(errors)[:5]

    labels = [e[1] for e in topFive]
    mostCommon = Counter(labels).most_common(1)[0][0]
    commonCount = labels.count(mostCommon)

    if commonCount >= 2:
      best = (mostCommon, 0)

    return best[0]

class EigenAverage(Classifier):
  def updateModel(self, patterns, weights):
    self.weights = weights
    self.patterns = patterns
    self.model.components_ = patterns


  def __init__(self, classes, numPatterns, width, height):
    super(EigenAverage, self).__init__(classes)

    self.patterns = None
    self.weights = None
    self.width = width
    self.height = height

    self.model = decomposition.NMF(n_components=numPatterns, init="random", random_state=0, solver="mu", max_iter=10000)

    M = [np.ones(self.width*self.height)]
    self.model.fit(M)

  def classify(self, file):
    M1 = [[eigenNFC.imageToVector(file, x=(256-self.width)//2, y=0, width=self.width, height=self.height)]]
    M = np.concatenate(M1)
    W = self.model.transform(M)

    errors = []
    for w in self.weights:
      arr = np.array(w[1], dtype=np.float32)
      error = np.linalg.norm(arr - W[0])
      errors.append( (error,w[0]))

    labels = set([w[0] for w in self.weights])

    averages = []
    for sp in labels:
      distances = [e[0] for e in errors if e[1] == sp]
      distances = sorted(distances)[:3]
      averages += [(sum(distances)/len(distances),sp)]

    averages = sorted(averages)
    return averages[0][1]

"""
    AMRElist = [e for e in errors if e[1] == "AMRE"]
    BBWAlist = [e for e in errors if e[1] == "BBWA"]
    BTBWlist = [e for e in errors if e[1] == "BTBW"]
    CHSPlist = [e for e in errors if e[1] == "CHSP"]
    COYElist = [e for e in errors if e[1] == "COYE"]
    OVENlist = [e for e in errors if e[1] == "OVEN"]
    SAVSlist = [e for e in errors if e[1] == "SAVS"]

    topAMRE = sorted(AMRElist)[:3]
    topBBWA = sorted(BBWAlist)[:3]
    topBTBW = sorted(BTBWlist)[:3]
    topCHSP = sorted(CHSPlist)[:3]
    topCOYE = sorted(COYElist)[:3]
    topOVEN = sorted(OVENlist)[:3]
    topSAVS = sorted(SAVSlist)[:3]

    allClasses = topAMRE+topBBWA+topBTBW+topCHSP+topCOYE+topOVEN+topSAVS
    i=0
    bestAvg = 999
    bestInd = 0
    while i < len(allClasses):
      sumClass =(allClasses[i][0]+allClasses[i+1][0]+allClasses[i+2][0])/3
      if sumClass < bestAvg:
        bestAvg = sumClass
        bestInd = i
      i+=3

    best = (allClasses[bestInd][1], 0)
    return best[0]
"""
