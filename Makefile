USERROOT=$(HOME)/sleepybox
LIBS=-lImlib2
LIBS+= -lX11
PULSELIBS=-lpulse-simple

service-install: service-dirs service-files	service-start
service-reload: service-stop service-files-remove service-files service-start
user-install: user-dirs user-files user-restart
user-reload: user-files-remove user-files user-restart
user-clean: user-files-remove 

screenshot:
	$(CC) -fpic -shared -I/usr/include/X11 $(LIBS) -DDEBUG user/usermetrics/screenshot.c -o user/usermetrics/screenshot.so
	
pasample:
	$(CC) -fpic -shared -I/usr/include/pulse $(PULSELIBS) user/usermetrics/pulseaudiosample.c -o user/usermetrics/pasample.so


service-dirs:
	mkdir /usr/share/sleepybox
	mkdir /usr/share/sleepybox/metrics
	mkdir /etc/sleepybox
	mkdir /var/log/sleepybox

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

service-stop: 
	-systemctl stop sleepybox.service
	systemctl disable sleepybox.service
	
service-files-remove:
	systemctl  disable sleepybox.service
	rm -f /usr/share/sleepybox/modules/*
	rm -f /usr/share/sleepybox/*.py
	rm -f /etc/sleepybox/*
	rm -f /var/log/sleepybox/*
	rm -f /lib/systemd/system/sleepybox.service
	rm -f /etc/dbus-1/system.d/org.lovi9573.sleepybox.conf
	
service-dirs-remove:
	rm -fR /usr/share/sleepybox
	rm -fR /etc/sleepybox
	rm -fR /var/log/sleepybox	


user-dirs:
	mkdir $(USERROOT)  #this prevents each new process from seeing the old one's pid file (its on a different inode)
	mkdir $(USERROOT)/metrics
	if [ ! -d "$(HOME)"/.config/systemd ]; then mkdir "$(HOME)"/.config/systemd; fi
	if [ ! -d "$(HOME)"/.config/systemd/user ]; then mkdir "$(HOME)"/.config/systemd/user; fi

user-files: screenshot pasample
	python setup.py
	###### user service ######
	#cp sleepybox.conf $(USERROOT)
	cp user/usermodules.conf $(USERROOT)/modules.conf
	cp common/*.py $(USERROOT)/
	cp user/sleepybox.py $(USERROOT)/
	cp user/usermetrics/*.py $(USERROOT)/metrics/
	cp user/usermetrics/*.so $(USERROOT)/metrics/
	cp user/sleepybox-user.service $(HOME)/.config/systemd/user/
	

user-restart:
	#python $(USERROOT)/sleepybox.py &
	systemctl --user enable sleepybox-user.service
	systemctl --user start sleepybox-user.service

user-dirs-remove:
	rm -rf $(USERROOT)

user-files-remove:
	systemctl --user disable sleepybox-user.service
	rm -rf $(USERROOT)/*.py
	rm -rf $(USERROOT)/*.pyc
	rm -rf $(USERROOT)/*.conf
	rm -rf $(USERROOT)/metrics/*
	rm -f $(HOME)/.config/systemd/user/sleepybox-user.service

#TODO: Write systemd --user & to .profile
