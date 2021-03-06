import suspendmetric




class Metric(suspendmetric.suspendmetric):
    jiffies = [0,0]
    jiffies_old = [0,0]
    
    def __init__(self,config):
        self.config = config
        super(Metric,self).__init__()
        
    
    def getSample(self):
       f = open("/proc/stat","r")
       js = map(int, f.readline().split()[1:])
       self.jiffies[1] += sum(js)
       self.jiffies[0] += js[0] + js[1] + js[2]
       cpuave = max([0, float(self.jiffies[0]-self.jiffies_old[0])/(self.jiffies[1] - self.jiffies_old[1]) ])
       self.jiffies_old = self.jiffies
       self.jiffies = [0,0]
       return float(cpuave) 
   
    def getUnits(self):
       return "/1.000"

    def getFormatting(self):
       return ":4.3f"
