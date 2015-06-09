

Dependencies
------------
gcc
libX11
libX11 headers
imlib2
imlib2 headers
pulseaudio-libs
pulseaudio-libs-devel

python PIL
python ctypes
libXss

Installation
------------
There are two parts to installation:

1. Run "make service-install" as root to install the systemd sleepybox service

2. Run "make user-install" as each user you would like to have a daemon running for.

Log Files
---------
Service wide level logs can be found in /var/log/sleepybox/sleepybox.log

User level logs can be found at $HOME/sleepybox/sleepybox.log
