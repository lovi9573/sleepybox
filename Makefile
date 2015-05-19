

reload: uninstall install

install:
	mkdir /usr/share/sleepybox
	cp ./*.py /usr/share/sleepybox
	mkdir /usr/share/sleepybox/metrics
	cp ./metrics/* /usr/share/sleepybox/metrics
	mkdir /etc/sleepybox
	cp sleepyboxsettings /etc/sleepybox
	cp cutoffs /etc/sleepybox
	mkdir /var/log/sleepybox
	cp sleepybox.service /lib/systemd/system
	systemctl --system daemon-reload
	systemctl start sleepybox.service
	
uninstall:
	systemctl stop sleepybox.service
	rm -fR /usr/share/sleepybox
	rm -fR /etc/sleepybox
	rm -fR /var/log/sleepybox
	rm -f /lib/systemd/system/sleepybox.service	