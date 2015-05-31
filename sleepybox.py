import gobject
import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
import datetime
from config import getConfig,getCutoffs
import threading
import os
from os.path import join
import sys
from subprocess import call
import getpass

HOME = os.getenv('HOME')
USERLOGFILE=join(HOME,'sleepybox/sleepybox.log')
CONFIGFILE=join(HOME,'sleepybox/sleepybox.conf')
CUTOFFSFILE=join(HOME,'sleepybox/cutoffs')
METRICSPATH = join(HOME,'sleepybox/metrics')

SLEEP=1
SCREENOFF=2



class SleepyBoxUserService(dbus.service.Object):
    def __init__(self):
        self.config = getConfig(CONFIGFILE)
        self.cutoffs = getCutoffs(CUTOFFSFILE)
        self.modules = {}
        for modulename in [f.strip(".py") for f in os.listdir(METRICSPATH) if (f[-3:] == ".py" and f[:8] != "__init__")]:
            with open(USERLOGFILE,"a") as fout:
                fout.write("loading {}\n".format(modulename))
            try:
                self.modules[modulename] = __import__("metrics."+modulename,globals(),locals(),['Metric'], -1).Metric(self.cutoffs[modulename]['weight'])
            except:
                with open(USERLOGFILE,"a") as fout:
                    fout.write("{} unable to load\n".format(modulename)) 
                    fout.write(str(sys.exc_info()[0])) 
        bus = dbus.SystemBus()
        proxy = bus.get_object('org.lovi9573.sleepyboxservice', '/org/lovi9573/sleepyboxservice',False)
        proxy.connect_to_signal('signal', self.check, 'org.lovi9573.sleepyboxservice')
        self.serviceIface = dbus.Interface(proxy,'org.lovi9573.sleepyboxservice')
        bus = dbus.SessionBus()
        proxy = bus.get_object('org.gnome.ScreenSaver', '/org/gnome/ScreenSaver')
        self.screenIface = dbus.Interface(proxy,'org.gnome.ScreenSaver')


    def check(self,t):
        with open(USERLOGFILE,"a") as fout:
            fout.write("check\n")
        sleep = True
        screenoff = True
        with open(USERLOGFILE,"a") as fout:
            for modulename, module in [(a,b) for a,b in self.modules.iteritems() if a in self.cutoffs.keys()]:
                #fout.write("reading from {}\n".format(modulename))
                #fout.flush()
                try:
                    v = module.getMetric(1)
                    cSleep = self.cutoffs.get(modulename,{}).get('sleepcut',0.0)
                    cScreen = self.cutoffs.get(modulename,{}).get('screencut',0.0)
                    fmt = module.getFormatting()
                    units = module.getUnits()
                    #fout.write(units+" "+fmt+" "+str(cSleep)+" "+str(cScreen)+" "+str(v)+" Checkpoint\n")
                    #fout.flush()
                    fout.write(("\t{}: {"+fmt+"} {} sleep:{"+fmt+"},screen:{"+fmt+"}\n").format(modulename,v,units,cSleep,cScreen))
                    sleepcut = v < cSleep
                    screencut = v < cScreen
                    if self.cutoffs.get(modulename,{}).get('a/b','b') == 'a':
                        sleepcut = not sleepcut
                        screencut = not screencut
                    if not sleepcut:
                        sleep = False
                    if not screencut:
                        screenoff = False
                except:
                    fout.write("Error encountered while processing {}\n\t{}\n".format(modulename,sys.exc_info()[0]))
                    del self.modules[modulename]
            if not sleep and t == SLEEP:
                self.serviceIface.veto(getpass.getuser())
            elif screenoff:
                self.doScreenOff()
            #fout.write("ending check\n")
        

   
    def doScreenOff(self):
        with open(USERLOGFILE,"a") as fout:
            fout.write("[{}] Initiating Screen Shutdown \n".format(datetime.datetime.now().__str__() ))
        #TODO: shutdown screen
        #self.screenIface.Lock()


if __name__ == "__main__":
    with open(USERLOGFILE,'w') as fout:
        fout.write("[{}] Starting sleepybox service user daemon \n".format(datetime.datetime.now().__str__() ))
    DBusGMainLoop(set_as_default=True)
    myservice = SleepyBoxUserService()
    gobject.threads_init()
    loop = gobject.MainLoop()
    loop.run()
