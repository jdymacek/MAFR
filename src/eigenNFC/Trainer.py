import MAFR
import eigenNFC
import numpy as np
from sklearn import decomposition
import sys

class Trainer:
  def __init__(self, files, patternNum):
    self.files = files
    self.patternNum = patternNum
    self.model = decomposition.NMF(n_components=self.patternNum, init="random", random_state=0, max_iter=100000, solver="mu")

  def train(self):
    print("ERROR MUST BE OVERWRITTEN BY SUBCLASS")
    sys.exit(1)


