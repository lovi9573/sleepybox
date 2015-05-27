USERROOT=$(HOME)/sleepybox

reload: uninstall install

install:
	###### system service ######
	mkdir /usr/share/sleepybox
	cp ./*.py /usr/share/sleepybox
	mkdir /usr/share/sleepybox/metrics
	cp ./metrics/* /usr/share/sleepybox/metrics
	#cp ./metrics/cpumetric.py /usr/share/sleepybox/metrics
	#cp ./metrics/__init__.py /usr/share/sleepybox/metrics
	mkdir /etc/sleepybox
	cp sleepybox.conf /etc/sleepybox
	cp cutoffs /etc/sleepybox
	#cp sleepybox.service.evn /etc/sysconfig/sleepybox
	mkdir /var/log/sleepybox
	cp sleepybox.service /lib/systemd/system/
	cp org.lovi9573.sleepybox.conf /etc/dbus-1/system.d/
	systemctl --system daemon-reload
	systemctl start sleepybox.service

userinstall:
	###### user service ######
	mkdir $(USERROOT)
	cp sleepybox.conf $(USERROOT)
	cp cutoffs $(USERROOT)
	mkdir $(USERROOT)/metrics
	cp ./usermetrics/*.py $(USERROOT)/metrics


	
uninstall: stop remove userremove

remove:	
	rm -fR /usr/share/sleepybox
	rm -fR /etc/sleepybox
	rm -fR /var/log/sleepybox
	rm -f /lib/systemd/system/sleepybox.service
	rm -f /etc/dbus-1/system.d/org.lovi9573.sleepybox.conf	

userremove:
	rm -rf $(USERROOT)

stop:
	systemctl stop sleepybox.service
