"""
Initial draft setup procedure to collect network interface and sound channel settings.
written by: Jesse Lovitt

"""

import subprocess
import stat
import os
from os.path import expanduser
import re

CONFIG_FILE = "usermodules.conf"

def getNetworkInterfaces():
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
    return interfaces


def getPulseAudioSources():
    #TODO: This doesn't quite work right.
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
    return channels
                    
                    
def getVMs(): 
    #Get VirtualBox machines to shutdown
    try:
        tmp = subprocess.check_output(["VBoxManage","list","vms"])
        print tmp
        vms = []
        for line in tmp.split("\n"):
            if len(line.strip()) > 0 and line.strip()[0] =="\"":
                m = re.search(r"\"(.+?)\"", line)
                if m:
                    vms.append( m.group(1) )
    except(OSError):
        vms = ""
    return vms
  
def getNetworkPreference(interfaces):
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
    return net           

def getPulseAudioPreference(channels):
    e_channels = list(enumerate(channels.keys()))
    n = -1
    snd = ""
    while n > len(e_channels) or n < 0:
        print "The following sound channels have been found."
        for e_c in e_channels:
            print e_c[0]," : ",channels[e_c[1]][1]
        n = int(raw_input("Choose a channel to monitor for sound activity:"))
        if n <= len(e_c) and n >= 0:
            snd = channels[e_channels[n][1]][0]
    return snd


def writeConfig(config):
    with open(os.path.join(os.getcwd(),CONFIG_FILE), "w") as fout:
        for module in config.keys():
            fout.write(config[module]['comments'])
            fout.write("["+module+"]\n")
            for key,keylist in config[module]['keys'].iteritems():
                for keydict in keylist:
                    if len(keydict['comments']) > 0:
                        fout.write(keydict['comments'])
                    fout.write(key+" "+keydict['value']+"\n")
            fout.write("\n")
                
                
def readConfig():
    config = {}
    currentmodule = ""
    comments = ""
    with open(os.path.join(os.getcwd(),CONFIG_FILE), "r") as fin:
        for line in fin:
            if len(line.strip()) > 0 and line.strip()[0] == "[":
                currentmodule = line.strip().strip("[]")
                if currentmodule not in config.keys():
                    config[currentmodule] = {'keys':{}, 'comments': comments}
                comments = ""
            elif line[0] == "#":
                comments += line + "\n"
            elif len(line.strip()) > 0:
                key,val = line.strip().split()
                config[currentmodule]['keys'][key] = []
                config[currentmodule]['keys'][key].append({'value':val,'comments': comments})
                comments = ""
    return config          
 
 
def putKeyVal(module,key,val,config):
    #TODO: Don't allow repeats
    if module not in config.keys():
        config[module] = {'keys':{}, 'comments': ""} 
    if key not in config[module]['keys'].keys():
        config[module]['keys'][key] =  []
        config[module]['keys'][key].append({'value':val,'comments': ""})
        return config
    config[module]['keys'][key].append({'value': val, 'comments':''})       
    return config

def setKeyVal(module,key,val,config):
    if module not in config.keys():
        config[module] = {'keys':{}, 'comments': ""} 
    if key not in config[module]['keys'].keys():
        config[module]['keys'][key] =  []
    config[module]['keys'][key].append({'value':val,'comments': ""})
    return config


if __name__ == "__main__":      
    config = readConfig()
    config = setKeyVal('soundmetric','sink_name', getPulseAudioPreference(getPulseAudioSources()), config)
    for vm in getVMs():
        config = putKeyVal('virtualbox', 'vm_name', vm, config)
    writeConfig(config) 
    print "\nSettings written to ", CONFIG_FILE
