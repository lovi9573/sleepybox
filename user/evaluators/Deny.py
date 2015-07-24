'''
Created on Jul 18, 2015

@author: user
'''

from base import EvaluatorBase

class Evaluator(EvaluatorBase):
    '''
    Default evaluator.
    Machine and screen always on
    '''


    def __init__(self, cutoffs):
        '''
        Constructor
        Accepts a module configuration dictionary
        '''
        pass
    
    def eval(self, metrics):
        return {'sleep':False,
                'screenoff':False}
        