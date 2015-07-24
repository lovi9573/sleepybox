'''
Created on Jul 18, 2015

@author: user
'''

from base import EvaluatorBase

class Evaluator(EvaluatorBase):
    '''
    This Evaluator requires the following for each module
    [<module_name>]
    suspend    <int>
    screen    <int>
    new_weight <int>
    when     <'above'/'below'>
    '''


    def __init__(self, cutoffs):
        '''
        Constructor
        Accepts a module configuration dictionary
        '''
        self.cutoffs = cutoffs
    def eval(self, metrics):
        sleep = True
        screenoff = True
        for modulename,metric in metrics.iteritems():
            cSleep = float(self.cutoffs.get(modulename,{}).get('suspend',0.0))
            cScreen = float(self.cutoffs.get(modulename,{}).get('screen',0.0))
            sleepcut = metric.get('v',0) < cSleep
            screencut = metric.get('v',0) < cScreen
            if self.cutoffs.get(modulename,{}).get('when','below') == 'above':
                sleepcut = not sleepcut
                screencut = not screencut
            if not sleepcut:
                sleep = False
            if not screencut:
                screenoff = False    
        return {'sleep':sleep,
                'screenoff':screenoff}
        