from Classifier import Classifier
import MAFR
from sklearn import cluster
from sklearn import linear_model
from sklearn import preprocessing
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

    best = ("UNKN", 9999)
    for w in self.weights:
      arr = np.array(w[1], dtype=np.float32)
      #guess = w[0].split("/")[0]
      guess = w[0]
      #use normalized coefficients
      q = W[0] / np.linalg.norm(W[0])

      error = np.linalg.norm(arr - q)
      if error < best[1]:
        best = (guess, error)

    return best[0]



class EigenMultiCluster(Classifier):
  def updateModel(self, patterns, weights):
    self.weights = weights
    self.patterns = patterns
    self.model.components_ = patterns

    number_clusters = 200
    self.clusters = {}

    for c in self.classes:   
        X = np.concatenate([[np.array(w[1], dtype=np.float64) for w in self.weights if w[0].split("/")[0] == c]])
        number_clusters = min(200,len(X)//2)
        self.clusters[c] = cluster.KMeans(n_clusters=number_clusters).fit(X)


  def __init__(self, classes, numPatterns, width, height):
    super(EigenMultiCluster, self).__init__(classes)

    self.patterns = None
    self.weights = None
    self.clusters = None
    self.width = width
    self.height = height
    self.threshold = 0.7

    self.model = decomposition.NMF(n_components=numPatterns, init="random", random_state=0, solver="mu", max_iter=10000)

    M = [np.ones(self.width*self.height)]
    self.model.fit(M)


  def classify(self, file):
    M1 = [[eigenNFC.imageToVector(file, x=(256-self.width)//2, y=0, width=self.width, height=self.height)]]
    M = np.concatenate(M1)
    W = self.model.transform(M)
    if sum(W[0]) == 0:
        print("no signal\t", file)
        return "????"      

    W[0] = W[0]/sum(W[0])

    ps = []
    for c in self.classes:
        predicted = self.clusters[c].predict([W[0]])[0]
        ps += [(np.linalg.norm(self.clusters[c].cluster_centers_[predicted]-W[0]),c)]

    sortedP = sorted(ps)
    #if sortedP[0][0] >= self.threshold:
    #   return sortedP[0][1]
    return sortedP[0][1]

class EigenCluster(Classifier):
  def updateModel(self, patterns, weights):
    self.weights = weights
    self.patterns = patterns
    self.model.components_ = patterns
    y = [w[0].split("/")[0] for w in self.weights]
    X = np.concatenate([[np.array(w[1], dtype=np.float64) for w in self.weights]])

    number_clusters = 3000
    self.cluster = cluster.KMeans(n_clusters=number_clusters).fit(X)
    self.probs = [{c:0 for c in self.classes} for i in range(number_clusters)]
   
    for i in range(len(weights)):
        cluster_index = self.cluster.labels_[i]
        self.probs[cluster_index][weights[i][0]] = self.probs[cluster_index][weights[i][0]] + 1

#    for p in self.probs:
#        for c in self.classes:
#            print(c + ": ",p[c],"\t",end="")
#        print("")


  def __init__(self, classes, numPatterns, width, height):
    super(EigenCluster, self).__init__(classes)

    self.patterns = None
    self.weights = None
    self.cluster = None
    self.width = width
    self.height = height
    self.threshold = 0.7

    self.model = decomposition.NMF(n_components=numPatterns, init="random", random_state=0, solver="mu", max_iter=10000)

    M = [np.ones(self.width*self.height)]
    self.model.fit(M)


  def classify(self, file):
    M1 = [[eigenNFC.imageToVector(file, x=(256-self.width)//2, y=0, width=self.width, height=self.height)]]
    M = np.concatenate(M1)
    W = self.model.transform(M)
    W[0] = W[0]/sum(W[0])
    predicted = self.cluster.predict([W[0]])
    ps = [(self.probs[predicted[0]][c],c) for c in self.classes]

    sortedP = sorted(ps,reverse=True)
    #if sortedP[0][0] >= self.threshold:
    #   return sortedP[0][1]
    return sortedP[0][1]



class EigenBayes(Classifier):
  def updateModel(self, patterns, bayes):
    self.bayes = bayes
    self.patterns = patterns
    self.model.components_ = patterns


  def __init__(self, classes, numPatterns, width, height):
    super(EigenBayes, self).__init__(classes)
    self.patterns = None
    self.weights = None
    self.bayes = None
    self.width = width
    self.height = height
    self.model = decomposition.NMF(n_components=numPatterns, init="random", random_state=0, solver="mu", max_iter=10000)
    self.classes = classes

    M = [np.ones(self.width*self.height)]
    self.model.fit(M)

  def classify(self, file):
    M1 = [[eigenNFC.imageToVector(file, x=(256-self.width)//2, y=0, width=self.width, height=self.height)]]
    M = np.concatenate(M1)
    raw = self.model.transform(M)
    raw[0] = raw[0]/sum(raw[0])

    results = []
    for c in self.classes:
      results += [(self.bayes.pOf(raw[0],c),c)]

    results = sorted(results,reverse=True)

    return results[0][1]



class EigenRegression(Classifier):
  def updateModel(self, patterns, weights):
    self.weights = weights
    self.patterns = patterns
    self.model.components_ = patterns
    y = [w[0].split("/")[0] for w in self.weights]
    X = np.concatenate([[np.array(w[1], dtype=np.float64) for w in self.weights]])
    self.scaler = preprocessing.StandardScaler().fit(X)
    X_train = self.scaler.transform(X)
    self.reg = linear_model.LogisticRegression(random_state=0,max_iter=10000).fit(X_train, y)



  def __init__(self, classes, numPatterns, width, height):
    super(EigenRegression, self).__init__(classes)

    self.patterns = None
    self.weights = None
    self.reg = None
    self.width = width
    self.height = height

    self.threshold = 0.7

    self.model = decomposition.NMF(n_components=numPatterns, init="random", random_state=0, solver="mu", max_iter=10000)

    M = [np.ones(self.width*self.height)]
    self.model.fit(M)


  def classify(self, file):
    M1 = [[eigenNFC.imageToVector(file, x=(256-self.width)//2, y=0, width=self.width, height=self.height)]]
    M = np.concatenate(M1)
    raw = self.model.transform(M)
    raw[0] = raw[0]/sum(raw[0])
    #print(raw)
    #W = raw
    W = self.scaler.transform(raw)
    ps = zip(self.reg.predict_proba(W)[0],self.reg.classes_)
    sortedP = sorted(ps,reverse=True)
    #if sortedP[0][0] >= self.threshold:
    #   return sortedP[0][1]
    #return "UNKN"
    return sortedP[0][1]

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
    best = ("UNKN", 9999)
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

    return best[0]

class EigenAverage(Classifier):
  def updateModel(self, patterns, weights):
    self.weights = weights
    for idx, row in enumerate(self.weights):
      arr = np.array(row[1], dtype=np.float32)
      total = sum(arr)
      guess = row[0].split("/")[0]
      self.weights[idx] = (guess, arr/total, row[0])

    self.patterns = patterns
    self.model.components_ = patterns


  def __init__(self, classes, numPatterns, width, height, averageWidth=3):
    super(EigenAverage, self).__init__(classes)

    self.patterns = None
    self.weights = None
    self.width = width
    self.height = height
    self.averageWidth = averageWidth

    self.model = decomposition.NMF(n_components=numPatterns, init="random", random_state=0, solver="mu", max_iter=10000)

    M = [np.ones(self.width*self.height)]
    self.model.fit(M)

  def classify(self, file):
    M1 = [[eigenNFC.imageToVector(file, x=(256-self.width)//2, y=0, width=self.width, height=self.height)]]
    M = np.concatenate(M1)
    W = self.model.transform(M)

    errors = []
    for w in self.weights:
#arr = np.array(w[1], dtype=np.float32)
      row = W[0]/sum(W[0])
      error = np.linalg.norm(w[1] - row)
      errors.append( (error,w[0],w[2]))

    labels = set([w[0] for w in self.weights])

    averages = []
    for sp in labels:
      distances = [(e[0],e[2]) for e in errors if e[1] == sp]
      distances = sorted(distances)[:self.averageWidth]
      #print(distances)
      distances = [x[0] for x in distances]
      averages += [(sum(distances)/len(distances),sp)]

    averages = sorted(averages)

   # print(f"{averages[0][0]},{averages[1][0]},{averages[2][0]},{averages[0][1]}",end="")
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

class EigenVersus(Classifier):
  def updateModel(self, patterns, weights):
    self.weights = weights
    self.patterns = patterns
    self.model.components_ = patterns


  def __init__(self, classes, numPatterns, width, height):
    super(EigenVersus, self).__init__(classes)

    self.patterns = None
    self.weights = None
    self.width = width
    self.height = height
    self.species = classes[0]

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
      if w[0] != self.species:
        errors.append( (error,"REST"))
      else:
        errors.append( (error,self.species))

    errors = sorted(errors)
    return errors[0][1]
    labels = set([w[1] for w in errors])

    averages = []
    for sp in labels:
      distances = [e[0] for e in errors if e[1] == sp]
      distances = sorted(distances)[:5]
      averages += [(sum(distances)/len(distances),sp)]

    averages = sorted(averages)
    return averages[0][1]

  def classifyAll(self, files):
    files.sort()
    self.confusion = {k:{k:0 for k in self.classes} for k in self.classes}
    for f in files:
      predicted = self.classify(f)
      expected = f.split("/")[-2]
      if expected != self.species:
        expected = "REST"

      self.confusion[expected][predicted] += 1
    self.accuracy = sum([self.confusion[k][k] for k in self.classes]) / len(files)
    for k in self.confusion.keys():
      total = sum(self.confusion[k].values())
      for sp in self.classes:
        self.confusion[k][sp] = round(self.confusion[k][sp] / total, 3)
    return self.accuracy

class EigenTrickle(Classifier):
  def updateModel(self, patterns, weights):
    self.weights = weights
    self.patterns = patterns
    self.model.components_ = patterns


  def __init__(self, classes, numPatterns, width, height):
    super(EigenTrickle, self).__init__(classes)

    self.patterns = None
    self.weights = None
    self.width = width
    self.height = height
    self.species = classes[0]

    self.model = decomposition.NMF(n_components=numPatterns, init="random", random_state=0, solver="mu", max_iter=10000)

    M = [np.ones(self.width*self.height)]
    self.model.fit(M)

  def classify(self, file):
    for c in self.classes:
      versus = EigenVersus([c,"REST"], len(self.patterns), self.width, self.height)
      versus.updateModel(self.patterns, self.weights)
