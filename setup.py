"""
Initial draft setup procedure to collect network interface and sound channel settings.
written by: Jesse Lovitt

"""

import subprocess
import stat
import os
from os.path import expanduser

if __name__ == "__main__":
	#Get network interface names and addresses
	interfaces = {}
	tmp = subprocess.check_output(["ifconfig"])
	c_if = ""
	for line in tmp.split("\n"):
		if line and line[0] != " ":
			c_if = line.split(":")[0]
			interfaces[c_if] = []
		else:
			line_c = line.split(" ")
			for i,c in enumerate(line_c):
				if c =="inet":
					interfaces[c_if].append(line_c[i+1])

	#Get sound channel to monitor
	channels = {}
	tmp = subprocess.check_output(["pactl","list"])	
	for section in tmp.split("\n\n"):
		lines = section.split("\n")
		if lines[0].strip()[0:6] == "Source":
			channels[lines[0]] = ["",""]
			for line in lines:
				l = line.strip().split(":")
				if l[0] == "Name":
					channels[lines[0]][0] = l[1].strip()
				elif l[0] == "Description":
					channels[lines[0]][1] = l[1]
				


	#Get VirtualBox machines to shutdown
	try:
		tmp = subprocess.check_output(["VBoxManage","list","vms"])
		vms = "("
		for line in tmp:
			if line.strip()[0] =="\"":
				vms += line.split("\"")[0]
		vms = vms.strip() + ")"
	except(OSError):
		vms = ""			
	
	#Get user preferences:
	e_interfaces = list(enumerate(interfaces.keys()))
	print "The following network interfaces have been found."
	for e_if in e_interfaces:
		print e_if[0] , ": ",e_if[1]," at ",interfaces[e_if[1]]
	n = int(raw_input("choose an interface number to monitor for network traffic:"))
	if len(e_if) <= n:
		net = e_interfaces[n][1]
	else:
		net = interfaces.keys()[0]
	print "\n\n\n"
	e_channels = list(enumerate(channels.keys()))
	print "The following sound channels have been found."
	for e_c in e_channels:
		print e_c[0]," : ",channels[e_c[1]][1]
	n = int(raw_input("Choose a channel to monitor for sound activity:"))
	if len(e_c) <= n:
		snd = channels[e_channels[n][1]][0]
	else:
		snd = channels.values()[0][0] 

	#Write settings to disk
	suspendpath = os.path.normpath(os.path.join(os.path.realpath(__file__),".."))	
	fn = os.path.join(suspendpath,"sleepyboxsettings.sh")	
	fh = open(fn,"r")
	settings = fh.readlines()
	for i,line in enumerate(settings):
		if line[0:7] == "NETCARD":
			settings[i] ="NETCARD="+net+"\n"
		if line[0:9] == "SOUNDCARD":
			settings[i] = "SOUNDCARD="+snd+"\n"
		if line[0:9] == "VBMACHINE" and vms != "":
			settings[i] = "VBMACHINE="+vms+"\n"
	fh = open(fn,"w")
	fh.writelines(settings)
	print "" 
	print "Settings written to ", fn

	#Add startup / kill script to .session
	home = expanduser("~")
	dirn = os.path.join(home,".session")
	if not os.path.exists(dirn):
		os.makedirs(dirn)
	fn = os.path.join(dirn, "cansuspend")	
	fh = open(fn, "w")
	script = """#/bin/bash

if [ "$1" = 'presession' ]; then
  #Start the smart suspend script
  #CSPID=$(cat "$HOME/suspend/pid")
  #if [ -n "$CSPID" ]; then
  #  kill $CSPID &>> "$HOME/suspend/cansuspenderror.log"	
  #fi
  if [ -e "$HOME/suspend/run" ]; 
  then
    :
  else
    touch $HOME/suspend/run
    $HOME/suspend/sleepyboxd &>> /home/user/suspend/cansuspenderror.log &
  fi
  echo "sleepybox started"
fi

if [ "$1" = 'postsession' ]; then
  #Stop the smart suspend script
  echo \"Shutdown\n\" >> \"$HOME/suspend/cansuspend.log\"
  CSPID=$(cat \"$HOME/suspend/pid\")
  #kill $CSPID &>> \"$HOME/suspend/cansuspenderror.log\"
  rm $HOME/suspend/run 
  echo "sleepybox stopped"
fi

"""
	fh.writelines([script])
	os.fchmod(fh.fileno(), 511)
	print "Startup line written to ~/.session/cansuspend"
	print ""
	print "*** Don't forget to run setupgdm.py with root permissions"
	print "*** You must also comment out the line 'Defaults requiretty' using visudo"


	
	


