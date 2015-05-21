import gobject
import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
import datetime
from config import getConfig,getCutoffs

LOGFILE='/var/log/sleepybox'
CONFIGFILE='/etc/sleepybox/sleepybox.conf'
CUTOFFSFILE='/etc/sleepybox/cutoffs'

class SleepyBoxService(dbus.service.Object):
    def __init__(self):
	self.vetos = False
	self.config = getConfig(CONFIGFILE)
	self.cutoffs = getCutoffs(CUTOFFSFILE)
	self.modules = {}
	for file in [f.strip(".py") for f in os.listdir("/usr/share/sleepybox/metrics") if f[-3:] == ".py"]:
		self.modules[f] = __import__("metrics."+f,globals(),locals(),['Metric'], -1).Metric()
        bus_name = dbus.service.BusName('org.lovi9573.sleepyboxservice', bus=dbus.SystemBus())
        dbus.service.Object.__init__(self, bus_name, '/org/lovi9573/sleepyboxservice')
	threading.Timer(self.config.get("POLLTIME",120),self.check).start()

    def check(self):
	sleep = True
	screenoff = True
	for modulename, module in [(a,b) for a,b in self.Modules.iteritems() if a in self.cutoffs.keys()]:
		v = module.getMetric()
		sleepcut = v < self.cutoffs[modulename]['sleepcut']
		screencut = v < self.cutoffs[modulename]['screencut']
		if self.cutoffs[modulename]['a/b'] == 'a':
			sleepcut = not sleepcut
			screencut = not screencut
		if not sleepcut:
			sleep = False
		if not screencut:
			screenoff = False
	if sleep:
		with open(LOGFILE,"a") as fout:
			fout.write("[{}] Sleep requested\n".format(datetime.datetime.now().__str__() ))
		threading.Timer(20, self.doSleep).start()		
		self.signal()
	elif screenoff:
		with open(LOGFILE,"a") as fout:
			fout.write("[{}] Screen shutdown requested\n".format(datetime.datetime.now().__str__() ))
		threading.Timer(20, self.doScreenOff).start()		
		self.signal()  #TODO: different types of signals.
	

    @dbus.service.method('org.lovi9573.sleepyboxservice')
    def veto(self,who):
	with open(LOGFILE,"a") as fout:
		fout.write("[{}] Sleep veto'd by {}\n".format(datetime.datetime.now().__str__() , who))
	self.vetos = True

    @dbus.service.signal(dbus_interface='com.lovi9573.sleepyboxservice',signature='')
    def signal(self):
	pass

    def doSleep(self):
	if not self.vetos:
		with open(LOGFILE,"a") as fout:
			fout.write("[{}] Initiating Sleep \n".format(datetime.datetime.now().__str__() ))
		self.vetos = False
		#TODO: sleep
	self.vetos = False
   
    def doScreenOff(self):
	if not self.vetos:
		with open(LOGFILE,"a") as fout:
			fout.write("[{}] Initiating Screen Shutdown \n".format(datetime.datetime.now().__str__() ))
		self.vetos = False
		#TODO: shutdown screen
	self.vetos = False


if __name__ == "__main__":
	with open(LOGFILE,'w') as fout:
		fout.write("[{}] Starting sleepybox service daemon \n".format(datetime.datetime.now().__str__() ))
	DBusGMainLoop(set_as_default=True)
	myservice = SleepyBoxService()
	loop = gobject.MainLoop()
	loop.run()
