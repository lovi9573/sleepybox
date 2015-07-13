
import suspendmetric

class Metric(suspendmetric.suspendmetric):
    bytes = 0
    bytes_old = 0
    
    def __init__(self,config):
        self.config = config
        super(Metric,self).__init__()
        self.getSample()
    
    def getSample(self):
        with open("/proc/net/dev","r") as f:
            f.readline()
            f.readline()
            self.bytes = 0
            line = f.readline()
            while( line != ""):
                cols = line.split(":")[1].split()
                self.bytes += int(cols[0]) + int(cols[8])
                line = f.readline()
        dBytes = self.bytes - self.bytes_old
        self.bytes_old = self.bytes
        return float(dBytes/1024/int(self.config.get('POLLTIME',1)))
    
    def getUnits(self):
        return "ave kB/s"
    
    def getFormatting(self):
        return ":>5.0f"
    
