# naiveBayes.py
# -------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import util
import classificationMethod
import math
import numpy as np
from copy import deepcopy

a = "O"

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

  # def calcc(self, trainingSetLabelFeature, trainingSetLabel, probabil, k, ii, jj):
  #   probabil[ii][jj] = ((trainingSetLabelFeature[ii][jj] + k) / (trainingSetLabel[ii][a] + (k * 2)))
  #   return float(probabil[ii][jj])

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

    totalCount = util.Counter()
    trainingSetLabelFeature = {}
    trainingSetLabelFeature = util.Counter()  # this is c(f,y) and util.Counter() gives it all labels
    trainingsFeatures = util.Counter()
    trainingSetLabel = util.Counter() # this is c(f',y)
    trainingSetPriorDist = util.Counter()

    #Note: if you dont add them equaal to util.Counter() and to an empty object you get "key Error"
    condProb = util.Counter() #keeping it empty for now


    #This sets to the corresponding labels and features
    for i in self.legalLabels:
      trainingSetLabel[i] = util.Counter()
      trainingSetPriorDist[i] = util.Counter()
      trainingSetLabelFeature[i] = util.Counter() #this is to set it equal to labels
      condProb[i]={} # this is to set probCond equal to labels

    ### NOTE : The reason all objects are set to util.Counter and {} is to escape error in initialization
    ## if you set it to just util.Counter it does not adds up in the list

    j=0
    totalNCounts = len(trainingData)

    # Here we use the already set labels to the trainedData for pairing

    for i in range(len(trainingData)):
       label = trainingLabels[i]
       feats = trainingData[i]
    for i in range(len(trainingData)):
       label = trainingLabels[i]
       for j in range(len(trainingData)):
         trainingSetLabel[label][a] = trainingSetLabel[label][a] + 1  # counts total labels and sets which labels will be marked in features
         trainingSetLabelFeatre = deepcopy(trainingLabels)
         #trainingSetLabelFeature[label][a] = trainingSetLabelFeature[label][a] + 1  # adds labels to features in to their positions
    for i in range(len(trainingData)):
      label = trainingLabels[i]
      feats = trainingData[i]
      trainingSetLabelFeature[label][a] = trainingSetLabelFeature[label][a] + 1#feats[c]  # adds labels to features in to their positions
      for c in self.features:  # sets features and labels
          trainingSetLabelFeature[label][c] = trainingSetLabelFeature[label][c] + feats[c]
    for i in range(len(trainingData)):
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
          #condProb2[i][j] = self.calcc(trainingSetLabelFeature, trainingSetLabel, condProb2, k, i, j)
          #conditional[label]= self.calcc(trainingSetLabelFeature, trainingSetLabel, conditional, k, i, j)
          #print trainingSetLabelFeature

      # def calcc(self, trainingSetLabelFeature, trainingSetLabel, probabil, k, ii, jj):
      #   probabil[ii][jj] = ((trainingSetLabelFeature[ii][jj] + k) / (trainingSetLabel[ii][a] + (k * 2)))
      #   return float(probabil[ii][jj])

      for i in self.legalLabels:
        trainingSetPriorDist[i] = float(trainingSetLabelFeature[i][a])/float((totalNCounts)) # P(Y)=c/n

      self.trainningData = deepcopy(trainingData)
      self.trainingSetPriorDist = trainingSetPriorDist
      self.condProb = condProb
      pred = self.classify(validationData)

      # m = 0
      # for i in range(len(pred)):
      #   if (pred[i] != validationLabels[i]):
      #     m = m + 1
      # print m
      # NumberOfTest = float(len(validationLabels))
      # predictionError = (m / NumberOfTest) * 100.00
      # print "Prediction Error: ", predictionError
      print "program end3"


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
          #self.errrx = self.errrx + 1
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


    
      
