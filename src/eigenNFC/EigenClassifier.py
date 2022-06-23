from Classifier import Classifier
import MAFR
from sklearn import decomposition
import numpy as np
import csv
import eigenNFC
import sys

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
    M1 = [[eigenNFC.imageToVector(file, x=72, y=0, width=self.width, height=self.height)]]
    M = np.concatenate(M1)
    W = self.model.transform(M)

    best = ("JUNK", 9999)
    for w in self.weights:
      arr = np.array(w[1], dtype=np.float32)
      guess = w[0]
      error = np.linalg.norm(arr - W[0])
      if error < best[1]:
        best = (guess, error)

    return best[0]
