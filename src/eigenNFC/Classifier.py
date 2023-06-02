import sys
import math

#base class for classifiers, will be overwritten by subclasses
class Classifier:
  def __init__(self, classes):
    self.classes = classes
    self.acccuracy = 0.0
    self.confusion = {k:{k:0 for k in self.classes} for k in self.classes}
    self.labelsUsed = {}
  
  def classify(self, file):
    print("ERROR: MUST BE OVERWRITTEN BY SUBCLASS")
    sys.exit(1)

  #correct label is directory
  def classifyAll(self, files):
    files.sort()
    self.confusion = {k:{k:0 for k in self.classes} for k in self.classes}
    

    for f in files:
#print(f)
      result = self.classify(f)

      predicted = result.split("/")[0]

      expected = f.split("/")[-2]
#      print("," + expected)

      self.confusion[expected][predicted] += 1
      if result not in self.labelsUsed:
         self.labelsUsed[result] = (0,0)
      if expected == predicted:
         self.labelsUsed[result] = (self.labelsUsed[result][0] + 1,self.labelsUsed[result][1]) 
      else:
         self.labelsUsed[result] = (self.labelsUsed[result][0],self.labelsUsed[result][1] + 1)


#    for x,y in self.labelsUsed.items():
#      print(f"{x}\t{y[0]}\t{y[1]}")
#    for sp in self.classes:
#       print("\t"+sp,end="\t")
#    print("")
#
#    for k in self.confusion.keys():
#       print(f"{k}",end="\t")
#       for sp in self.classes:
#          print(f"{self.confusion[k][sp]}",end='\t')
#       print("")

    for k in self.classes:
      p = 0
      r = 0
      mcc = 0
      tp = self.confusion[k][k]
      fp = sum([self.confusion[x][k] for x in self.classes ]) - tp
      fn = sum([self.confusion[k][x] for x in self.classes ]) - tp
      tn = len(files) - (tp+fp+fn)

      a = max(tp+fp,1)
      b = max(tp+fn,1)
      c = max((math.sqrt((tp+fp)*(tp+fn)*(tn+fp)*(tn+fn))),1)

      p = tp/a
      r = tp/b
      mcc = ((tp*tn)-(fp*fn))/c

      acc = (tp+tn)/(tp+tn+fp+fn)

      print("{:5.4f}\t{:5.4f}\t{:5.4f}".format(r,p,acc),end="\t")

    print("")


    self.accuracy = sum([self.confusion[k][k] for k in self.classes]) / len(files)
    for k in self.confusion.keys():
      total = sum(self.confusion[k].values())
      for sp in self.classes:
        if total != 0:
          self.confusion[k][sp] = round(self.confusion[k][sp] / total, 3)
    return self.accuracy

