USERROOT=$(HOME)/sleepybox
LIBS=-lImlib2
LIBS+= -lX11
PULSELIBS=-lpulse-simple

service-install: service-dirs service-files	service-start
service-reload: service-stop service-files-remove service-files service-start
user-install: user-dirs user-files user-restart
user-reload: user-files-remove user-files user-restart


screenshot:
	$(CC) -fpic -shared -I/usr/include/X11 $(LIBS) -DDEBUG usermetrics/screenshot.c -o usermetrics/screenshot.so
	
pasample:
	$(CC) -fpic -shared -I/usr/include/pulse $(PULSELIBS) usermetrics/pulseaudiosample.c -o usermetrics/pasample.so


service-dirs:
	mkdir /usr/share/sleepybox
	mkdir /usr/share/sleepybox/metrics
	mkdir /etc/sleepybox
	mkdir /var/log/sleepybox

service-files: 
	###### system service ######
	cp ./*.py /usr/share/sleepybox
	cp ./metrics/* /usr/share/sleepybox/metrics
	#cp ./metrics/cpumetric.py /usr/share/sleepybox/metrics
	#cp ./metrics/__init__.py /usr/share/sleepybox/metrics
	cp sleepybox.conf /etc/sleepybox
	cp modules.conf /etc/sleepybox
	#cp sleepybox.service.evn /etc/sysconfig/sleepybox
	cp sleepybox.service /lib/systemd/system/
	cp org.lovi9573.sleepybox.conf /etc/dbus-1/system.d/

service-start:
	systemctl enable sleepybox.service
	systemctl --system daemon-reload
	systemctl start sleepybox.service

service-stop: 
	-systemctl stop sleepybox.service
	systemctl disable sleepybox.service
	
service-files-remove:
	rm -fR /usr/share/sleepybox/*
	rm -fR /etc/sleepybox/*
	rm -fR /var/log/sleepybox/*
	rm -f /lib/systemd/system/sleepybox.service
	rm -f /etc/dbus-1/system.d/org.lovi9573.sleepybox.conf
	
service-dirs-remove:
	rm -fR /usr/share/sleepybox
	rm -fR /etc/sleepybox
	rm -fR /var/log/sleepybox	


user-dirs:
	mkdir $(USERROOT)  #this prevents each new process from seeing the old one's pid file (its on a different inode)
	mkdir $(USERROOT)/metrics

user-files: screenshot pasample
	python setup.py
	###### user service ######
	#cp sleepybox.conf $(USERROOT)
	cp usermodules.conf $(USERROOT)/modules.conf
	cp sleepybox.py $(USERROOT)/
	cp suspendmetric.py $(USERROOT)/
	cp utility.py $(USERROOT)/
	cp config.py $(USERROOT)/
	cp ./usermetrics/*.py $(USERROOT)/metrics/
	cp ./usermetrics/*.so $(USERROOT)/metrics/

user-restart:
	python $(USERROOT)/sleepybox.py &

user-dirs-remove:
	rm -rf $(USERROOT)

user-files-remove:
	rm -rf $(USERROOT)/*.py
	rm -rf $(USERROOT)/*.pyc
	rm -rf $(USERROOT)/*.conf
	rm -rf $(USERROOT)/metrics/*


