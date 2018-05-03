
  def calcc(self,trainingSetLabelFeature,probabil,k,ii,jj):
    probabil[ii][jj] = (trainingSetLabelFeature[ii][jj] + k) / (trainingSetLabelFeature[ii][a] + (k * 2))
    return probabil[ii][jj]

  def tt(self, trainingData, trainingLabels, validationData, validationLabels, kgrid):
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
    trainingSetLabelFeature = util.Counter()  # this is c(f,y) and util.Counter() gives it all labels
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
    # for i in range( len(trainingData) ):
    #   label = trainingLabels[i]
    #   #trainingSetLabel[label][1]= trainingSetLabel[label][1] + 1
    #   trainingSetLabel[label][1] = trainingSetLabel[label][1] + 1


    # for i in range( len(trainingData) ):
    #   label = trainingLabels[i]
    #   feats = trainingData[i]
    #
    #   for j in range( len(trainingData) ):
    #     trainingSetLabel[label][1] = trainingSetLabel[label][1] + 1 #counts total labels
    #     trainingSetLabelFeature[label][a]=trainingSetLabelFeature[label][a] + 1 #adds labels to features in to their positions
    #
    #
    #
    #   for c in self.features: #sets features and labels
    #       trainingSetLabelFeature[label][c] = trainingSetLabelFeature[label][c] + feats[c]
    #       # reason i decided to add feat instead of 1 above is when i added 1 it kept giving me to 0 pixels
    #       # where as this always comes down to solid features


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
      trainingSetLabelFeature[label][a] = trainingSetLabelFeature[label][a] + 1  # adds labels to features in to their positions
      for c in self.features:  # sets features and labels
        trainingSetLabelFeature[label][c] = trainingSetLabelFeature[label][c] + feats[c]
        # reason i decided to add feat instead of 1 above is when i added 1 it kept giving me to 0 pixels
        # where as this always comes down to solid features

    #print trainingSetLabelFeature

    setLabelFeature = deepcopy(trainingSetLabelFeature)
    setLabel = deepcopy(trainingSetLabelFeature)
    condProb2 = deepcopy(condProb)
    conditional = deepcopy(condProb)

    for k in kgrid:
      for i in self.legalLabels:
        for j in self.features:
          condProb[i][j] = (trainingSetLabelFeature[i][j] + k) / (trainingSetLabelFeature[i][a] + (k*2))
          condProb2[i][j] = self.calcc(trainingSetLabelFeature, condProb, k, i, j)#(trainingSetLabelFeature[i][j] + k) / (trainingSetLabelFeature[i][a] + (k * 2))
          conditional[label]= self.calcc(trainingSetLabelFeature, condProb, k, i, j)#(trainingSetLabelFeature[i][j] + k) / (trainingSetLabelFeature[i][a] + (k*2))



      for i in self.legalLabels:
        trainingSetPriorDist[i] = float(trainingSetLabelFeature[i][a])/float((totalNCounts)) # P(Y)=c/n


      self.trainningData = deepcopy(trainingData)
      self.trainingSetPriorDist = trainingSetPriorDist
      self.condProb = condProb

      incrm = 0
      sizeVD = len(validationData)

      for i in range(sizeVD): # loop to search for the same labels we have in validationData
        pred = self.classify(validationData[i])
        if (pred[i] == validationLabels[i]):
         for i in (self.legalLabels):
           for j in (self.features):
             condProb[i][j] = self.calcc(trainingSetLabelFeature, condProb, k, i, j)


      #self.calculateLogJointProbabilities(validationData,trainingData,trainingSetPriorDist,condProb)
    # for i in range(sizelength):
    #   labels = trainingLabels[i]
    #   trainingSetLabel[labels] = trainingSetLabel[labels] + 1
    #   #NOTE: REASON FOR (j,Label) is data presence in dataset which is basically -> [(a,b) , c]
    #   for j in self.features: # for i,j in self.features: trainingSetLabelFeature[(j,labels)][i]
    #     trainingSetLabelFeature[(j,labels)] = trainingSetLabelFeature[(j,labels)] + 1
    #     totalCount[(j,labels)] = trainingSetLabelFeature[(j,labels)] #NOT SURE ABOUT THIS:THIS IS JUST IN CASE FOR THE TOTAL SUMMATION
   #
   #  for i in range(len(trainingData)):
   #    datum = trainingData[i]
   #    label = trainingLabels[i]
   #    trainingSetLabel[label] += 1
   #    for (featvalue) in datum.keys():
   #      totalCount[feat][label]+= 1
   #        trainingSetLabelFeature[feat][label] += 1
   #  print "trainingSetLabelFeature: \n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n", trainingSetLabelFeature
   #
   # # print "trainingSetLabelFeature",trainingSetLabelFeature
   #
   #  for i in range(sizelength):
   #    labels2 = trainingLabels[i]
   #    trainingSetPriorDist[labels2] = trainingSetPriorDist[labels2] + 1
   #
   #  print "%^^^^^^^^ trainingSetPriorDist"
   #  #print trainingSetPriorDist
   #
   #
   #
   # # print trainingSetLabelFeature
   #
   #  for k in kgrid:
   #    for i in self.legalLabels:
   #      for j in self.features:
   #        condProb[(i,j)] = (trainingSetLabelFeature[(i,j)] + k)/(0.0 + trainingSetLabel[i] + 2*k )
   #
   #
   #
   #
   # # print "condProb", condProb
   #
   #  #print condProb
   #  trainingSetPriorDist.normalize()
   #  self.trainingSetPriorDist = trainingSetPriorDist
   #  self.condProb= condProb
   #  #print self.condProb
   #  #print self.trainingSetPriorDist
   #
   #  # conditionalProb2= util.Counter()
   #  # for lb,ft in condProb.items():
   #  #   conditionalProb2[lb] = conditionalProb2[lb] + ft
   #  #   #print conditionalProb2[lb]
   #
   #  # conditionalProb = util.Counter()
   #  # for lb,ft in condProb.items():
   #  #   conditionalProb[ft] = conditionalProb[ft] + lb
   #    #print conditionalProb[ft]
   #
   #
   # # print conditionalProb
   #  print "hell-oz"
   #
   #
   #  accuracy = correct / len(self.classify(validationData))
   #
   #  print "percent is : ",accuracy
   #
   #
   #  self.trainingSetPriorDist = trainingSetPriorDist
   #  self.trainingSetPriorDist, self.condProb

 # def
 
  def ccc(self, datum):
    """
    Returns the log-joint distribution over legal labels and the datum.
    Each log-probability should be stored in the log-joint counter, e.g.
    logJoint[3] = <Estimate of log( P(Label = 3, datum) )>

    To get the list of all possible features or labels, use self.features and
    self.legalLabels.
    """
    logJoint = util.Counter()

    fC=util.Counter()
    for i in range( len(self.trainningData) ):
      fC=self.trainningData[i]

    for i in self.legalLabels:
      logJoint[i] = ( math.log(self.trainingSetPriorDist[i]) )
      #print "in log:"
      #print logJoint[i]
      for j in self.features:
        if(fC[j]==True ): #if the features are present in training data then calculate the data
          #Above mean if the value in the feature pixel is 0 it would be false not counted if
          #probabilityForTHECONDITIONALS = condProb[i][j]
          logJoint[i] =  logJoint[i] + math.log(self.condProb[i][j])
        else:
          logJoint[i] = logJoint[i] + math.log(1 - self.condProb[i][j])

    # for i in self.legalLabels:
    #   logargmax = math.log(conditionals[i])
    return logJoint
  
 
