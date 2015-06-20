import math

class suspendmetric(object):
    
    def __init__(self):
        self.weight = max(min(float(self.config.get('new_weight',1)),1.0),0.0)
        self.t = int(self.config.get('POLLTIME',1))
        self.metric = 0.0

    def getSample(self):
        return 0.0
    
    def getMetric(self):
        s = self.getSample()  
        w_old = math.pow((1.0-self.weight),self.t)
        w_new = 1.0 - w_old
        self.metric = w_new*s + w_old*self.metric  
        return self.metric,s
        
    def getUnits(self):
        return ""
    
    def getFormatting(self):
        return ""
    
    def setup(self):
        pass