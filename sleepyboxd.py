import gobject
import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
import datetime

class SleepyBoxService(dbus.service.Object):
    def __init__(self):
	self.vetos = False
        bus_name = dbus.service.BusName('org.lovi9573.sleepyboxservice', bus=dbus.SystemBus())
        dbus.service.Object.__init__(self, bus_name, '/org/lovi9573/sleepyboxservice')

    @dbus.service.method('org.lovi9573.sleepyboxservice')
    def sleep(self,who):
	with open("/var/log/sleepybox","a") as fout:
		fout.write("[{}] Sleep requested by {}\n".format(datetime.datetime.now().__str__() , who))
	threading.Timer(20, self.doSleep).start()		
	self.signal()
	

    @dbus.service.method('org.lovi9573.sleepyboxservice')
    def veto(self):
	with open("/var/log/sleepybox","a") as fout:
		fout.write("[{}] Sleep veto'd by {}\n".format(datetime.datetime.now().__str__() , who))
	self.vetos = True

    @dbus.service.signal(dbus_interface='com.lovi9573.sleepyboxservice',signature='')
    def signal(signal):
	pass

    def doSleep(self):
	if not self.vetos:
		with open("/var/log/sleepybox","a") as fout:
			fout.write("[{}] Initiating Sleep \n".format(datetime.datetime.now().__str__() ))
		self.vetos = False
		#TODO: sleep
	self.vetos = False

if __name__ == "__main__":
	DBusGMainLoop(set_as_default=True)
	myservice = SleepyBoxService()
	loop = gobject.MainLoop()
	loop.run()
