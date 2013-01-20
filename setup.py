"""
Initial draft setup procedure to collect network interface and sound channel settings.
written by: Jesse Lovitt

"""

import subprocess
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
	curr_chan = ""
	for line in tmp.split("\n"):
		if line and line[0] != " " and line.strip()[0:6] == "Source":
			curr_chan = line			
			channels[line] = ["" , ""]
		elif curr_chan != "":
			line_c = line.lstrip().split(":")
			if line_c[0] == "Name":
				channels[curr_chan][0] = line_c[1].lstrip()
			elif line_c[0] == "Description":
				channels[curr_chan][1] = line_c[1]
			
	
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
	fn = os.path.join(suspendpath,"cansuspendsettings.sh")	
	fh = open(fn,"r")
	settings = fh.readlines()
	for i,line in enumerate(settings):
		if line[0:7] == "NETCARD":
			settings[i] ="NETCARD="+net+"\n"
		if line[0:9] == "SOUNDCARD":
			settings[i] = "SOUNDCARD="+snd+"\n"
	fh = open(fn,"w")
	fh.writelines(settings)
	print "" 
	print "Settings written to ", fn

	#Add startup line to .bash_profile
	home = expanduser("~")
	fn = os.path.join(home,".bash_profile")
	fh = open(fn, "r")
	profile = fh.readlines()
	start_found = False
	for line in profile:
		if "cansuspend" in line:
			start_found = True
	if not start_found:
		fh = open(fn, "a")
		fh.writelines(["#Start the smart suspend script\n",os.path.join(suspendpath,"cansuspend") + " &> "+os.path.join(suspendpath,"cansuspenderror.log")+" &"])
		print "Startup line written to .bash_profile"

	
	


