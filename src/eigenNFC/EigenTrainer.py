from Trainer import Trainer
import MAFR
import eigenNFC
import numpy as np

class SimpleTrainer(Trainer):
  def __init__(self, files, patternNum, height=0, width=0):
    super(SimpleTrainer, self).__init__(files, patternNum)
    self.height = height
    self.width = width
    self.weights = None

  def updateSize(self, height, width):
    self.height = height
    self.width = width

  def weightsAsString(self):
      rv = ""
      for w in self.weights:
        
        rv += w[0] + ","
        rv += ",".join(w[1])
        
        
      return rv 

  def train(self):
    ml = []
    labels = []

    for f in self.files:
      labels.append(f.split("/")[-2])
      arr = eigenNFC.imageToVector(f, x=(256-self.width)//2, y=0, width=self.width, height=self.height)
      ml += [[arr]]
    M = np.concatenate(ml) 

    w = self.model.fit_transform(M)

    self.weights = []
    for index, row in enumerate(w):
      if sum(row) > 0:
          self.weights.append((labels[index],np.round(row/sum(row), decimals=4)))
      else:
          print(labels[index], row)
    
    h = self.model.components_
    return(self.weights, h)
