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
import daemon
#import lockfile
from pidfile import PidFile
import signal

HOME = os.getenv('HOME')
DAEMON_ROOT = join(HOME,'sleepybox')
USERLOGFILE=join(HOME,'sleepybox/sleepybox.'+datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+'.log')
USERERRFILE=join(HOME,'sleepybox/error.log')
GLOBALCONFIGFILE=join('/etc/sleepybox/sleepybox.conf')
CONFIGFILE=join(DAEMON_ROOT,'user.conf')
MODULE_CONFIG_FILE=join(HOME,'sleepybox/modules.conf')
METRICSPATH = join(HOME,'sleepybox/metrics')
PIDFILE = join(HOME,'sleepybox/sleepybox.pid')

SLEEP=1
SCREENOFF=2



class SleepyBoxUserService(dbus.service.Object):
    def __init__(self):
        self.config = getConfig(GLOBALCONFIGFILE)
        print self.config
        self.config.update(getConfig(CONFIGFILE))
        print self.config
        self.moduleconfig = getModuleConfig(MODULE_CONFIG_FILE)
        evaluator_name = self.config.get('EVALUATOR',"Deny")
        self.evaluatorconfig = getModuleConfig(join(DAEMON_ROOT,evaluator_name+".conf"))
        self.modules = {}
        for modulename in [f.strip(".py") for f in os.listdir(METRICSPATH) if (f[-3:] == ".py" and f[:8] != "__init__")]:
            with open(USERLOGFILE,"a") as fout:
                fout.write("loading {}\n".format(modulename))
            try:
                self.modules[modulename] = __import__("metrics."+modulename,globals(),locals(),['Metric'], -1).Metric(self.moduleconfig[modulename])
            except Exception as e:
                with open(USERLOGFILE,"a") as fout:
                    fout.write("{} unable to load: {}\n".format(modulename,traceback.format_exc()))
                    fout.write("{} \n".format(str(e)))  
                    #fout.write(str(sys.exc_info()[0])) 
                    traceback.print_exc(file = fout)
        self.config["modules"] = self.modules.keys()
        self.evaluator = __import__("evaluators."+evaluator_name,globals(),locals(),['Evaluator'],-1).Evaluator(self.moduleconfig)
        bus = dbus.SystemBus()
        proxy = bus.get_object('org.lovi9573.sleepyboxservice', '/org/lovi9573/sleepyboxservice',False)
        proxy.connect_to_signal('signal', self.check, 'org.lovi9573.sleepyboxservice')
        proxy.connect_to_signal('signalsleeptime', self.handle_signalsleeptime, 'org.lovi9573.sleepyboxservice')
        self.serviceIface = dbus.Interface(proxy,'org.lovi9573.sleepyboxservice')
        bus = dbus.SessionBus()
        proxy = bus.get_object('org.gnome.ScreenSaver', '/org/gnome/ScreenSaver')
        self.screenIface = dbus.Interface(proxy,'org.gnome.ScreenSaver')


    def check(self,t):
        with open(USERLOGFILE,"a") as fout:
            fout.write("\n[{}]  ".format(datetime.datetime.now().__str__() ))
            metrics = {}
            for modulename, module in [(a,b) for a,b in self.modules.iteritems() if a in self.moduleconfig.keys()]:
                #fout.write("reading from {}\n".format(modulename))
                #fout.flush()
                try:
                    v,s = module.getMetric()
                    #TODO: remove the section that makes a decision here and put it behind an interface
                    #TODO: interface input: dictionary modulename=>metric
                    #TODO: interface output: dictionary {suspend,screen,...}=>{t/f}
                    fmt = module.getFormatting()
                    units = module.getUnits()
                    #fout.write(units+" "+fmt+" "+str(cSleep)+" "+str(cScreen)+" "+str(v)+" Checkpoint\n")
                    #fout.flush()
                    metrics[modulename] = {'v':v,'s':s}
                    fout.write(("{}:{"+fmt+"}({"+fmt+"}){} ; ").format(modulename,v,s,units))
                except Exception as e:
                    fout.write("Error encountered while processing {}\n\t{}\n".format(modulename,traceback.format_exc()))
                    fout.write("{}\n".format(str(e)))
                    del self.modules[modulename]
            evaluation = self.evaluator.eval(metrics)
            if t == SLEEP:
                if evaluation.get('sleep',False):
                    self.serviceIface.accept(getpass.getuser())
                else:
                    self.serviceIface.veto(getpass.getuser())
                if evaluation.get('screenoff',False):
                    self.doScreenOff()
            elif t == SCREENOFF:
                if evaluation.get('screenoff',False):
                    self.doScreenOff()
        

   
    def doScreenOff(self):
        with open(USERLOGFILE,"a") as fout:
            fout.write("\n[{}] Initiating Screen Shutdown \n".format(datetime.datetime.now().__str__() ))
        if self.config.get('ENABLE',0) == '1':
            #self.screenIface.Lock()
            call(["xset", "dpms", "force", "standby"])

    def handle_signalsleeptime(self,time):
        self.evaluator.update(time)

if __name__ == "__main__":
    context = daemon.DaemonContext(working_directory=DAEMON_ROOT,
                                   pidfile=PidFile(PIDFILE))
    
    #context.signal_map = { signal.SIGTERM: program_cleanup,
    #                       signal.SIGHUP: 'terminate' }
    
    #logfile = open(USERLOGFILE,'w')
    #context.files_preserve = [logfile]
    
       
    """
    if os.path.isfile(PIDFILE):
        pid = -1
        with open(PIDFILE,"r") as fin:
            pid = int(fin.readline())
        try:
            os.kill(pid, signal.SIGKILL)
        except:
            with open(USERERRFILE,'w') as fout:
                fout.write("[{}] Stale PID file found. Existing sleepybox service not stopped. \n".format(datetime.datetime.now().__str__() ))
    with open(PIDFILE,'w') as fout:
        fout.write(str(os.getpid()));
    """
    #with context:
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
