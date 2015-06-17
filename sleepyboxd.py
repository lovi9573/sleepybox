import gobject
import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
import datetime
from config import getConfig,getModuleConfig
import threading
import time
import os
import sys
from subprocess import call

LOGFILE='/var/log/sleepybox/sleepybox.log'
CONFIGFILE='/etc/sleepybox/sleepybox.conf'
CUTOFFSFILE='/etc/sleepybox/modules.conf'

SLEEP=1
SCREENOFF=2

class PerpetualTimer(threading.Thread):
    def __init__(self,event,timeout,function):
        threading.Thread.__init__(self)
        self.stopped = event
        self.time = timeout
        self.callback = function

        
    def run(self):
        while not self.stopped.wait(self.time):
            self.callback()


class SleepyBoxService(dbus.service.Object):
    def __init__(self):
        self.vetos = False
        self.responses = 0
        self.config = getConfig(CONFIGFILE)
        self.cutoffs = getModuleConfig(CUTOFFSFILE)
        self.modules = {}
        for modulename in [f.strip(".py") for f in os.listdir("/usr/share/sleepybox/metrics") if (f[-3:] == ".py" and f[:8] != "__init__")]:
            with open(LOGFILE,"a") as fout:
                fout.write("loading {} \n".format(modulename))
            try:
                self.modules[modulename] = __import__("metrics."+modulename,globals(),locals(),['Metric'], -1).Metric(self.cutoffs[modulename])
            except:
                with open(LOGFILE,"a") as fout:
                    fout.write("{} unable to load\n".format(modulename)) 
        bus=dbus.SystemBus()   
        #powerproxy = bus.get_object('org.freedesktop.UPower', "/org/freedesktop/UPower",False) 
        powerproxy = bus.get_object('org.freedesktop.login1', "/org/freedesktop/login1",False) 
        #self.powerIface = dbus.Interface(powerproxy,"org.freedesktop.UPower")           
        self.powerIface = dbus.Interface(powerproxy,"org.freedesktop.login1.Manager")           
        bus_name = dbus.service.BusName('org.lovi9573.sleepyboxservice', bus=bus)
        dbus.service.Object.__init__(self, bus_name, '/org/lovi9573/sleepyboxservice')
        self.timer = PerpetualTimer(threading.Event(),int(self.config.get("POLLTIME",120)),self.check)
        
    def start(self):
        self.timer.start()


    def check(self):
        sleep = True
        screenoff = True
        with open(LOGFILE,"a") as fout:
            fout.write("[{}]  ".format(datetime.datetime.now().__str__() ))
            for modulename, module in [(a,b) for a,b in self.modules.iteritems() if a in self.cutoffs.keys()]:
                #fout.write("reading from {}\n".format(modulename))
                #fout.flush()
                try:
                    v,s = module.getMetric(int(self.config.get("POLLTIME",120)))
                    cSleep = float(self.cutoffs.get(modulename,{}).get('suspend',0.0))
                    cScreen = float(self.cutoffs.get(modulename,{}).get('screen',0.0))
                    fmt = module.getFormatting()
                    units = module.getUnits()
                    #fout.write("\t{} read\n".format(modulename))
                    #fout.flush()
                    #fout.write(units+" "+fmt+" "+str(cSleep)+" "+str(cScreen)+" "+str(v)+" Checkpoint\n")
                    #fout.flush()
                    fout.write(("{}:{"+fmt+"}({"+fmt+"}){}[{}/{}] ; ").format(modulename,v,s,units,cSleep,cScreen))
                    sleepcut = v < cSleep
                    screencut = v < cScreen
                    if self.cutoffs.get(modulename,{}).get('when','below') == 'above':
                        sleepcut = not sleepcut
                        screencut = not screencut
                    if not sleepcut:
                        sleep = False
                    if not screencut:
                        screenoff = False
                except:
                    fout.write("Error encountered while processing {}\n\t{}\n".format(modulename,sys.exc_info()[0]))
                    del self.modules[modulename]
            if sleep:
                fout.write(" => Sleep requested\n")
                threading.Timer(int(self.config.get("RESPONSETIME",20)), self.doSleep).start()        
                self.signal(SLEEP)
                #time.sleep(int(self.config.get("RESPONSETIME",20)))
                #self.doSleep()
            elif screenoff:
                fout.write(" => Screen shutdown signalled\n")
                #threading.Timer(int(self.config.get("RESPONSETIME",20)), self.doScreenOff).start()        
                self.signal(SCREENOFF) 
            else:
                fout.write("\n")
            #fout.write("ending check\n")
        
    

    @dbus.service.method('org.lovi9573.sleepyboxservice')
    def veto(self,who):
        with open(LOGFILE,"a") as fout:
            fout.write("[{}] Sleep veto'd by {}\n".format(datetime.datetime.now().__str__() , who))
        self.vetos = True
        
    @dbus.service.method('org.lovi9573.sleepyboxservice')
    def accept(self,who):
        with open(LOGFILE,"a") as fout:
            fout.write("[{}] Sleep accepted by {}\n".format(datetime.datetime.now().__str__() , who))
        self.responses += 1

    @dbus.service.method('org.freedesktop.DBus.Introspectable')
    def Introspect(self, object_path, connection):
        return dbus.service.Object.Introspect(self, object_path, connection)

    @dbus.service.signal(dbus_interface='org.lovi9573.sleepyboxservice',signature='i')
    def signal(self,t):
        pass

    def doSleep(self):
        if not self.vetos and self.responses >= int(self.config.get('REQUIRED_RESPONSES', '0')):
            with open(LOGFILE,"a") as fout:
                fout.write("[{}] Initiating Sleep \n".format(datetime.datetime.now().__str__() ))
            self.vetos = False
            self.responses = 0
            #TODO: shutdown the VM's
            vms = [x.strip() for x in self.config.get("VBMACHINE","").split(",") if x.strip() !=""]
            for vm in vms:
                call(["VBoxManage"," controlvm {} savestate &> {}".format(vm,LOGFILE)])      
            if self.config.get('ENABLE',0)=="1":
                self.powerIface.Suspend(True)
        self.vetos = False
        self.responses = 0
   


if __name__ == "__main__":
    with open(LOGFILE,'w') as fout:
        fout.write("[{}] Starting sleepybox service daemon \n".format(datetime.datetime.now().__str__() ))
    gobject.threads_init()
    DBusGMainLoop(set_as_default=True)
    myservice = SleepyBoxService()
    myservice.start()
    #while(True):
        #TODO: put in a 'real' idle loop.
        #time.sleep(120)
    loop = gobject.MainLoop()
    loop.run()
