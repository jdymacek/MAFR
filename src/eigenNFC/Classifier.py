import sys

#base class for classifiers, will be overwritten by subclasses
class Classifier:
  def __init__(self, classes):
    self.classes = classes
    self.acccuracy = 0.0
    self.confusion = {k:{k:0 for k in self.classes} for k in self.classes}
  
  def classify(self, file):
    print("ERROR: MUST BE OVERWRITTEN BY SUBCLASS")
    sys.exit(1)

  #correct label is directory
  def classifyAll(self, files):
    files.sort()
    self.confusion = {k:{k:0 for k in self.classes} for k in self.classes}
    for f in files:
#print(f)
      predicted = self.classify(f)
      expected = f.split("/")[-2]
      print("," + expected)
      self.confusion[expected][predicted] += 1
    self.accuracy = sum([self.confusion[k][k] for k in self.classes]) / len(files)
    for k in self.confusion.keys():
      total = sum(self.confusion[k].values())
      for sp in self.classes:
        self.confusion[k][sp] = round(self.confusion[k][sp] / total, 3)
    return self.accuracy

