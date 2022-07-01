from Trainer import Trainer
import MAFR
import eigenNFC
import numpy as np

class SimpleTrainer(Trainer):
  def __init__(self, files, patternNum, height=0, width=0):
    super(SimpleTrainer, self).__init__(files, patternNum)
    self.height = height
    self.width = width

  def updateSize(self, height, width):
    self.height = height
    self.width = width

  def train(self):
    ml = []
    labels = []

    for f in self.files:
      labels.append(f.split("/")[-2])
      arr = eigenNFC.imageToVector(f, x=(256-self.width)//2, y=0, width=self.width, height=self.height)
      ml += [[arr]]
    M = np.concatenate(ml) 

    w = self.model.fit_transform(M)

    lines = []
    for index, row in enumerate(w):
      line = labels[index]
      for val in row:
        line += "," + str(np.round(val, decimals=7))
      line += "\n"
      lines.append(line)

    
    weights = []
    for line in lines:
      tokens = line.split(",")
      weights.append((tokens[0], tokens[1:]))

    h = self.model.components_
    return(weights, h)
