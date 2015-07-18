USERROOT=$(HOME)/sleepybox
LIBS=-lImlib2
LIBS+= -lX11
PULSELIBS=-lpulse-simple

service-install: service-dirs service-files	service-start
service-reload: service-uninstall service-install
user-install: user-dirs user-files user-start
user-reload: user-uninstall user-install


screenshot:
	$(CC) -fpic -shared -I/usr/include/X11 $(LIBS) -DDEBUG user/usermetrics/screenshot.c -o user/usermetrics/screenshot.so
	
pasample:
	$(CC) -fpic -shared -I/usr/include/pulse $(PULSELIBS) user/usermetrics/pulseaudiosample.c -o user/usermetrics/pasample.so


service-dirs:
	if [ ! -d /usr/share/sleepybox ]; then mkdir /usr/share/sleepybox; fi
	if [ ! -d /usr/share/sleepybox/metrics ]; then mkdir /usr/share/sleepybox/metrics; fi
	if [ ! -d /etc/sleepybox ]; then mkdir /etc/sleepybox; fi
	if [ ! -d /var/log/sleepybox ]; then mkdir /var/log/sleepybox; fi

service-files: 
	###### system service ######
	cp common/*.py /usr/share/sleepybox
	cp system/*.py /usr/share/sleepybox
	cp system/metrics/* /usr/share/sleepybox/metrics
	#cp ./metrics/cpumetric.py /usr/share/sleepybox/metrics
	#cp ./metrics/__init__.py /usr/share/sleepybox/metrics
	cp system/sleepybox.conf /etc/sleepybox
	cp system/modules.conf /etc/sleepybox
	#cp sleepybox.service.evn /etc/sysconfig/sleepybox
	cp system/sleepybox.service /lib/systemd/system/
	cp system/org.lovi9573.sleepybox.conf /etc/dbus-1/system.d/

service-start:
	systemctl enable sleepybox.service
	systemctl --system daemon-reload
	systemctl start sleepybox.service
	
service-uninstall:
	# stop the service
	-systemctl stop sleepybox.service
	systemctl  disable sleepybox.service
	# Remove directories
	rm -fR /usr/share/sleepybox
	rm -fR /etc/sleepybox
	rm -fR /var/log/sleepybox
	# Remove files	
	rm -f /lib/systemd/system/sleepybox.service
	rm -f /etc/dbus-1/system.d/org.lovi9573.sleepybox.conf
	


#
# User service
#

user-dirs:
	if [ ! -d $(USERROOT) ]; then mkdir $(USERROOT); fi  #this prevents each new process from seeing the old one's pid file (its on a different inode)
	if [ ! -d $(USERROOT)/metrics ]; then mkdir $(USERROOT)/metrics; fi
	#if [ ! -d "$(HOME)"/.config/systemd ]; then mkdir "$(HOME)"/.config/systemd; fi
	#if [ ! -d "$(HOME)"/.config/systemd/user ]; then mkdir "$(HOME)"/.config/systemd/user; fi

user-files: screenshot pasample
	python setup.py
	###### user service ######
	#cp sleepybox.conf $(USERROOT)
	cp user/usermodules.conf $(USERROOT)/modules.conf
	cp common/*.py $(USERROOT)/
	cp user/sleepybox.py $(USERROOT)/
	touch $(USERROOT)/sleepybox.log
	cp user/usermetrics/*.py $(USERROOT)/metrics/
	cp user/usermetrics/*.so $(USERROOT)/metrics/
	#cp user/sleepybox-user.service $(HOME)/.config/systemd/user/
	
user-start:
	#python $(USERROOT)/sleepybox.py &
	#systemctl --user enable sleepybox-user.service
	#systemctl --user start sleepybox-user.service
	#systemctl --user daemon-reload 

user-uninstall:
	#systemctl --user stop sleepybox-user.service
	#systemctl --user disable sleepybox-user.service
	rm -rf $(USERROOT)
	rm -f $(HOME)/.config/systemd/user/sleepybox-user.service


