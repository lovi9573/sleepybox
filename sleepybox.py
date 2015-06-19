import gobject
import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
import datetime
from config import getConfig,getModuleConfig
import os
import signal
import time
from os.path import join
import sys
from subprocess import call
import getpass
import traceback

HOME = os.getenv('HOME')
USERLOGFILE=join(HOME,'sleepybox/sleepybox.log')
CONFIGFILE=join('/etc/sleepybox/sleepybox.conf')
CUTOFFSFILE=join(HOME,'sleepybox/modules.conf')
METRICSPATH = join(HOME,'sleepybox/metrics')
PIDFILE = join(HOME,'sleepybox/pid')

SLEEP=1
SCREENOFF=2



class SleepyBoxUserService(dbus.service.Object):
    def __init__(self):
        self.config = getConfig(CONFIGFILE)
        self.cutoffs = getModuleConfig(CUTOFFSFILE)
        self.modules = {}
        for modulename in [f.strip(".py") for f in os.listdir(METRICSPATH) if (f[-3:] == ".py" and f[:8] != "__init__")]:
            with open(USERLOGFILE,"a") as fout:
                fout.write("loading {}\n".format(modulename))
            try:
                self.modules[modulename] = __import__("metrics."+modulename,globals(),locals(),['Metric'], -1).Metric(self.cutoffs[modulename])
            except:
                with open(USERLOGFILE,"a") as fout:
                    fout.write("{} unable to load\n".format(modulename)) 
                    #fout.write(str(sys.exc_info()[0])) 
                    traceback.print_exc(file = fout)
        bus = dbus.SystemBus()
        proxy = bus.get_object('org.lovi9573.sleepyboxservice', '/org/lovi9573/sleepyboxservice',False)
        proxy.connect_to_signal('signal', self.check, 'org.lovi9573.sleepyboxservice')
        self.serviceIface = dbus.Interface(proxy,'org.lovi9573.sleepyboxservice')
        bus = dbus.SessionBus()
        proxy = bus.get_object('org.gnome.ScreenSaver', '/org/gnome/ScreenSaver')
        self.screenIface = dbus.Interface(proxy,'org.gnome.ScreenSaver')


    def check(self,t):
        sleep = True
        screenoff = True
        with open(USERLOGFILE,"a") as fout:
            fout.write("\n[{}]  ".format(datetime.datetime.now().__str__() ))
            for modulename, module in [(a,b) for a,b in self.modules.iteritems() if a in self.cutoffs.keys()]:
                #fout.write("reading from {}\n".format(modulename))
                #fout.flush()
                try:
                    v,s = module.getMetric(int(self.config.get("POLLTIME",120)))
                    cSleep = float(self.cutoffs.get(modulename,{}).get('suspend',0.0))
                    cScreen = float(self.cutoffs.get(modulename,{}).get('screen',0.0))
                    fmt = module.getFormatting()
                    units = module.getUnits()
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
            if t == SLEEP:
                if sleep:
                    self.serviceIface.accept(getpass.getuser())
                else:
                    self.serviceIface.veto(getpass.getuser())
                if screenoff:
                    self.doScreenOff()
            elif t == SCREENOFF:
                if screenoff:
                    self.doScreenOff()
        

   
    def doScreenOff(self):
        with open(USERLOGFILE,"a") as fout:
            fout.write("\n[{}] Initiating Screen Shutdown \n".format(datetime.datetime.now().__str__() ))
        #TODO: shutdown screen
        if self.config.get('ENABLE',0) == '1':
            #self.screenIface.Lock()
            call(["xset", "dpms", "force", "standby"])


if __name__ == "__main__":
    if os.path.isfile(PIDFILE):
        pid = -1
        with open(PIDFILE,"r") as fin:
            pid = int(fin.readline())
        os.kill(pid, signal.SIGKILL)
    with open(PIDFILE,'w') as fout:
        fout.write(str(os.getpid()));
    with open(USERLOGFILE,'w') as fout:
        fout.write("[{}] Starting sleepybox service user daemon \n".format(datetime.datetime.now().__str__() ))
    DBusGMainLoop(set_as_default=True)
    myservice = SleepyBoxUserService()
    gobject.threads_init()
    #while(True):
        #TODO: put in a 'real' idle loop.
        #time.sleep(120)   
    loop = gobject.MainLoop()
    loop.run()
