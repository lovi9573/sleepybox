import suspendmetric
import utility
import os
# From https://github.com/Valodim/python-pulseaudio

from numpy.ctypeslib import ctypes


class Metric(suspendmetric.suspendmetric):
    
    def __init__(self,config):
        #TODO: get this from the setup script
        super(Metric,self).__init__(config.get('new_weight',1))
        self.sink_name = config.get('sink_name','')
        #self.sink_name = "alsa_output.pci-0000_00_1b.0.analog-stereo.monitor"
        self.padll = ctypes.cdll.LoadLibrary(os.path.join(os.path.dirname(__file__),'pasample.so'))
        self.padll.getPeak.restype = ctypes.c_float
        self.padll.getPeak.argtypes = [ctypes.c_char_p]
        
    
    def getSample(self,x):
       return self.padll.getPeak(self.sink_name)

   
    def getUnits(self):
       return "/1.00"

    def getFormatting(self):
       return ":3.2f"
   
if __name__ == "__main__":
    m = Metric('a')
    print m.getSample('a')