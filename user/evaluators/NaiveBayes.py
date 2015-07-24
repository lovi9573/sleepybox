'''
Created on Jul 19, 2015

@author: user
'''

import numpy as np
from base import EvaluatorBase
from sklearn.naive_bayes import GaussianNB
import pickle
import os

MODEL_FILE = "/home/user/sleepybox/metrics/naivebayes_model"

class Evaluator(EvaluatorBase):
    '''
    This Evaluator requires the following for each module
    [model]
    screenfile    naivebayes_screen_model
    sleepfile    naivebayes_sleep_model
    history        5
    minsleeptime    240
    minscreentime    240
    '''


    def __init__(self, config):
        '''
        Constructor
        Accepts a module configuration dictionary
        '''
        self.config = config
        self.historylen = config.get("model",{}).get("history",5)
        self.history = [0.0]*(len(self.modules)*self.historylen)
        #TODO: Discover these.
        self.modules = self.config.get("modules",[])
        self.modules = self.modules +['bias']
                                                  
        self.screenfile = config.get("model",{}).get("screenfile",os.environ.get("HOME")+"naivebayesscreenmodel")
        if os.path.isfile(self.screenfile):
            self.screenclassifier = pickle.load(self.screenfile)
        else:
            self.screenclassifier = GaussianNB()
            self.screenclassifier.fit(np.asarray(self.history, dtype = np.float32),np.zeros([1]))
        self.sleepfile = config.get("model",{}).get("sleepfile",os.environ.get("HOME")+"naivebayessleepmodel")
        if os.path.isfile(self.sleepfile):
            self.sleepclassifier = pickle.load(self.sleepfile)
        else:
            self.sleepclassifier = GaussianNB()
            self.sleepclassifier.fit(np.asarray(self.history, dtype = np.float32),np.zeros([1]))
        
    def eval(self, metrics):
        
        #preload expected inputs at 0.0
        inputs = {}
        for m in self.modules:
            inputs[m] = 0.0
        inputs['bias'] = 1.0
        #update given inputs
        for modulename,metric in metrics.iteritems():
            inputs[modulename] = metric
        #Transform into consistent order vector
        inputvector = []
        for inputname in sorted(self.modules):
            inputvector.append(inputs[inputname])
        self.history = self.history[0:-len(self.modules)] + inputvector
        npinvec = np.asarray(self.history, dtype=np.float32)
        sleepdecision = self.sleepclassifier.predict(npinvec)[0] == 1
        screendecision = self.sleepclassifier.predict(npinvec)[0] == 1
        return {'sleep':sleepdecision,
                'screenoff':screendecision}
        
    def update(self,timeslept, timescreenoff):
        #TODO: Use this knowledge about how long the sleep lasted to update the ML model.
        self.sleepclassifier.partial_fit(np.asarray(self.history, dtype=np.float32) ,
                                         np.asarray([timeslept > self.config.get("model",{}).get("minsleeptime",240)],dtype=np.int ))
        self.screenclassifier.partial_fit(np.asarray(self.history, dtype=np.float32) ,
                                         np.asarray([timescreenoff > self.config.get("model",{}).get("minscreentime",240)],dtype=np.int ))
        