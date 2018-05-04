import util
import classificationMethod
import math
import numpy as np
from copy import deepcopy

a = "marking"

class NaiveBayesClassifier(classificationMethod.ClassificationMethod):
  """
  See the project description for the specifications of the Naive Bayes classifier.
  
  Note that the variable 'datum' in this code refers to a counter of features
  (not to a raw samples.Datum).
  """
  def __init__(self, legalLabels):
    self.legalLabels = legalLabels
    self.type = "naivebayes"
    self.k = 1 # this is the smoothing parameter, ** use it in your train method **
    self.automaticTuning = False # Look at this flag to decide whether to choose k automatically ** use this in your train method **
    
  def setSmoothing(self, k):
    """
    This is used by the main method to change the smoothing parameter before training.
    Do not modify this method.
    """
    self.k = k

  def train(self, trainingData, trainingLabels, validationData, validationLabels):
    """
    Outside shell to call your method. Do not modify this method.
    """  
      
    # might be useful in your code later...
    # this is a list of all features in the training set.
    self.features = list(set([ f for datum in trainingData for f in datum.keys() ]));
    
    if (self.automaticTuning):
        kgrid = [0.001, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 20, 50]
    else:
        kgrid = [self.k]
        
    self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels, kgrid)


  def calcc(self,trainingSetLabelFeature,trainingSetLabel,probabil,k,ii,jj):
    probabil[ii][jj] = ((trainingSetLabelFeature[ii][jj] + k) / (trainingSetLabel[ii][a] + (k * 2)))
    return float(probabil[ii][jj])

  def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, kgrid):
    """
    Trains the classifier by collecting counts over the training data, and
    stores the Laplace smoothed estimates so that they can be used to classify.
    Evaluate each value of k in kgrid to choose the smoothing parameter
    that gives the best accuracy on the held-out validationData.

    trainingData and validationData are lists of feature Counters.  The corresponding
    label lists contain the correct label for each datum.

    To get the list of all possible features or labels, use self.features and
    self.legalLabels.
    """
    self.trainingData = trainingData
    totalCount = util.Counter()
    trainingSetLabelFeature = {}
    #trainingSetLabelFeature = util.Counter()  # this is c(f,y) and util.Counter() gives it all labels
    trainingsFeatures = util.Counter()
    trainingSetLabel = util.Counter() # this is c(f',y)
    trainingSetPriorDist = util.Counter()
    trainingSetLabelFeature2 = util.Counter()  # this is c(f',y)
    #Note: if you dont add them equaal to util.Counter() and to an empty object you get "key Error"
    condProb = util.Counter() #keeping it empty for now

    for i in self.legalLabels:
      trainingSetLabel[i] = util.Counter()
      trainingSetPriorDist[i] = util.Counter()
      trainingSetLabelFeature[i] = util.Counter() #this is to set it equal to labels
      condProb[i]={} # this is to set probCond equal to labels



    j=0
    #global a = 'marking'
    size = len(trainingData)
    totalNCounts = len(trainingData)

    for i in range(len(trainingData)):
       label = trainingLabels[i]
       feats = trainingData[i]
    for i in range(len(trainingData)):
       label = trainingLabels[i]
       for j in range(len(trainingData)):
         trainingSetLabel[label][a] = trainingSetLabel[label][a] + 1  # counts total labels and sets which labels will be marked in features
         trainingSetLabelFeatre = deepcopy(trainingLabels)
         #trainingSetLabelFeature[label][a] = trainingSetLabelFeature[label][a] + 1  # adds labels to features in to their positions
    for i in range(size):
      label = trainingLabels[i]
      feats = trainingData[i]
      trainingSetLabelFeature[label][a] = trainingSetLabelFeature[label][a] + 1#feats[c]  # adds labels to features in to their positions
      for c in self.features:  # sets features and labels
          trainingSetLabelFeature[label][c] = trainingSetLabelFeature[label][c] + feats[c]
    for i in range(size):
      label = trainingLabels[i]
      feats = trainingData[i]
      trainingSetLabel[label][a] = trainingSetLabel[label][a] + 1  # feats[c]  # adds labels to features in to their positions
      for c in self.features:  # sets features and labels
        trainingSetLabel[label][c] = trainingSetLabel[label][c] + 1
        # reason i decided to add feat instead of 1 above is when i added 1 it kept giving me to 0 pixels
        # where as this always comes down to solid features

    setLabelFeature = deepcopy(trainingSetLabelFeature)
    setLabel = deepcopy(trainingSetLabelFeature)
    condProb2 = deepcopy(condProb)
    conditional = deepcopy(condProb)

    for k in kgrid:
      for i in self.legalLabels:
        for j in self.features:
          condProb[i][j] = (trainingSetLabelFeature[i][j] + k) / (trainingSetLabel[i][j] + (k*2))#  trainingSetLabelFeature[i][a] + (k*2))
          condProb2[i][j] = self.calcc(trainingSetLabelFeature, trainingSetLabel, condProb2, k, i, j)
          #conditional[label]= self.calcc(trainingSetLabelFeature, trainingSetLabel, conditional, k, i, j)
      #print trainingSetLabelFeature

      for i in self.legalLabels:
        trainingSetPriorDist[i] = float(trainingSetLabelFeature[i][a])/float((totalNCounts)) # P(Y)=c/n

      self.trainningData = deepcopy(trainingData)
      self.trainingSetPriorDist = trainingSetPriorDist
      self.condProb = condProb
      pred = util.Counter()
      pred = self.classify(validationData)



      print "program end3"
      #pred2 = self.classify(validationData[i])
      #self.calculateLogJointProbabilities(validationData,trainingData,trainingSetPriorDist,condProb)
    # for i in range(sizelength):
    #   labels = trainingLabels[i]
    #   trainingSetLabel[labels] = trainingSetLabel[labels] + 1
    #   #NOTE: REASON FOR (j,Label) is data presence in dataset which is basically -> [(a,b) , c]
    #   for j in self.features: # for i,j in self.features: trainingSetLabelFeature[(j,labels)][i]
    #     trainingSetLabelFeature[(j,labels)] = trainingSetLabelFeature[(j,labels)] + 1
    #     totalCount[(j,labels)] = trainingSetLabelFeature[(j,labels)] #NOT SURE ABOUT THIS:THIS IS JUST IN CASE FOR THE TOTAL SUMMATION
   #
   # # print "trainingSetLabelFeature",trainingSetLabelFeature
   #
   #  for i in range(sizelength):
   #    labels2 = trainingLabels[i]
   #    trainingSetPriorDist[labels2] = trainingSetPriorDist[labels2] + 1
   #
   #  print "%^^^^^^^^ trainingSetPriorDist"
   #  #print trainingSetPriorDist
   # # print trainingSetLabelFeature
   #
   #  for k in kgrid:
   #    for i in self.legalLabels:
   #      for j in self.features:
   #        condProb[(i,j,k,o)] = (trainingSetLabelFeature[(i,j,j,k)] + k)/(0.0 + trainingSetLabel[i] + 2*k )
   # # print "condProb", condProb
   #  #print condProb
   #  trainingSetPriorDist.normalize()
   #  self.trainingSetPriorDist = trainingSetPriorDist
   #  self.condProb= condProb
   #  #print self.condProb
   #  #print self.trainingSetPriorDist
   #  # conditionalProb2= util.Counter()
   #    #print conditionalProb[ft]
   # # print conditionalProb
   #  print "hell-oz"
   #  print "percent is : "

   #  self.trainingSetPriorDist = trainingSetPriorDist
   #  self.trainingSetPriorDist, self.condProb


  def classify(self, testData):
    """
    Classify the data based on the posterior distribution over labels.
    
    You shouldn't modify this method.
    """
    guesses = []
    self.posteriors = [] # Log posteriors are stored for later data analysis (autograder).
    for datum in testData:
      posterior = self.calculateLogJointProbabilities(datum)
      guesses.append(posterior.argMax())
      self.posteriors.append(posterior)
    return guesses

  def calculateLogJointProbabilities(self, datum):
    """
    Returns the log-joint distribution over legal labels and the datum.
    Each log-probability should be stored in the log-joint counter, e.g.
    logJoint[3] = <Estimate of log( P(Label = 3, datum) )>

    To get the list of all possible features or labels, use self.features and
    self.legalLabels.
    """
    logJoint = util.Counter()
    #ignore the below part i was trying to use a different object to just store solid pixels
    #fC=util.Counter()
    #for i in range( len(self.trainningData) ):
     # fC[i]=self.datum[i].items()
    for i in self.legalLabels:
      logJoint[i] = float(( math.log(self.trainingSetPriorDist[i]) ))
      for j in self.features:
        if(datum[j]==True): #if the features are present in training data then calculate the data
          #Above mean if the value in the feature pixel is 0 it would be false not counted if
          #SEARCHES FOR SOLID PIXELS
          logJoint[i] =  logJoint[i] + math.log(self.condProb[i][j])
        else:
          logJoint[i] = logJoint[i] + math.log(1.0 - self.condProb[i][j])
          #Note: i usually get float errors if 0.0 is not used plus i noticed if pixel 0
          #was not dealt with I was getting weird errors crashes
    return logJoint
  
  def findHighOddsFeatures(self, label1, label2):
    """
    Returns the 100 best features for the odds ratio:
            P(feature=1 | label1)/P(feature=1 | label2)

    Note: you may find 'self.features' a useful way to loop through all possible features
    """
    featuresOdds = []

    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

    return featuresOdds


    
      
