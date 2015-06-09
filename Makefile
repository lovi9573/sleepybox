USERROOT=$(HOME)/sleepybox
LIBS=-lImlib2
LIBS+= -lX11
PULSELIBS=-lpulse-simple

reload: service-uninstall service-install
user-reload: user-uninstall user-install


screenshot:
	$(CC) -fpic -shared -I/usr/include/X11 $(LIBS) usermetrics/screenshot.c -o usermetrics/screenshot.so
	
pasample:
	$(CC) -fpic -shared -I/usr/include/pulse $(PULSELIBS) usermetrics/pulseaudiosample.c -o usermetrics/pasample.so


service-install:
	###### system service ######
	mkdir /usr/share/sleepybox
	cp ./*.py /usr/share/sleepybox
	mkdir /usr/share/sleepybox/metrics
	cp ./metrics/* /usr/share/sleepybox/metrics
	#cp ./metrics/cpumetric.py /usr/share/sleepybox/metrics
	#cp ./metrics/__init__.py /usr/share/sleepybox/metrics
	mkdir /etc/sleepybox
	cp sleepybox.conf /etc/sleepybox
	cp modules.conf /etc/sleepybox
	#cp sleepybox.service.evn /etc/sysconfig/sleepybox
	mkdir /var/log/sleepybox
	cp sleepybox.service /lib/systemd/system/
	cp org.lovi9573.sleepybox.conf /etc/dbus-1/system.d/
	systemctl --system daemon-reload
	systemctl start sleepybox.service

	

user-install: screenshot pasample
	python setup.py
	mkdir $(USERROOT)
	mkdir $(USERROOT)/metrics
	###### user service ######
	#cp sleepybox.conf $(USERROOT)
	cp usermodules.conf $(USERROOT)/modules.conf
	cp sleepybox.py $(USERROOT)/
	cp suspendmetric.py $(USERROOT)/
	cp utility.py $(USERROOT)/
	cp config.py $(USERROOT)/
	cp ./usermetrics/*.py $(USERROOT)/metrics/
	cp ./usermetrics/*.so $(USERROOT)/metrics/


	
service-uninstall: 
	-systemctl stop sleepybox.service
	rm -fR /usr/share/sleepybox
	rm -fR /etc/sleepybox
	rm -fR /var/log/sleepybox
	rm -f /lib/systemd/system/sleepybox.service
	rm -f /etc/dbus-1/system.d/org.lovi9573.sleepybox.conf	

user-uninstall:
	rm -rf $(USERROOT)


