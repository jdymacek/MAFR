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
    self.confusion = {k:{k:0 for k in self.classes} for k in self.classes}
    for f in files:
      predicted = self.classify(f)
      expected = f.split("/")[-2]
      self.confusion[predicted][expected] += 1
    self.accuracy = sum([self.confusion[k][k] for k in self.classes]) / len(files)
    return self.accuracy

