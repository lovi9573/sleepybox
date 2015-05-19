import utility
import suspendmetric

class netmetric(suspendmetric.suspendmetric):
    bytes = 0
    bytes_old = 0
    
    def getMetric(self,dTime):
        f = open("/proc/net/dev","r")
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
        return dBytes/1024/dTime
    
    def getUnits(self):
        return "ave kB/s"
    
    def getFormatting(self):
        return ":>4"
    
