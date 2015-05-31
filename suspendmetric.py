

class suspendmetric(object):
    
    def __init__(self, weight = 1.0):
        self.weight = max(min(weight,1.0),0.0)
        self.metric = 0.0

    def getSample(self,timeInterval):
        return 0.0
    
    def getMetric(self, timeInterval):
        s = self.getSample(timeInterval)
        self.metric = (1.0-self.weight)*self.metric + self.weight*s
        return self.metric,s
        
    def getUnits(self):
        return ""
    
    def getFormatting(self):
        return ""
    
    def setup(self):
        pass