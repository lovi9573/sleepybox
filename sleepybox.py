import time
import importlib
import glob
import re
import sys
import traceback
import dbus
import subprocess
import os


"""
TODOS:
Fix the above / below implementation
"""


if __name__ == "__main__":
    
    # Open the log files
    logfile = open("/var/log/sleepybox/sleepybox.log","w") 
    statuslogfile = open("/var/log/sleepybox/sleepyboxstatus.log","w")

    # Load metrics modules
    modules = {}
    files = glob.glob("/usr/share/sleepybox/metrics/*metric.py")
    r = re.compile('/usr/share/sleepybox/metrics/(.*).py')
    statuslogfile.write("Metrics Modules found:\n")
    for file in files:
        statuslogfile.write("\t"+file+"\n")
        m = r.match(file)
        name = "metrics."+m.group(1)
        mod = importlib.import_module(name)
        g = globals()
        modules[m.group(1)] = getattr(mod,m.group(1))()
        
    #Load global settings 
    settings = {}
    settingsfile = open("/etc/sleepybox/sleepyboxsettings","r")
    statuslogfile.write("Settings loaded:\n")
    for line in settingsfile:
        if (len(line.strip()) > 0 and line.strip()[0] !="#"):
            statuslogfile.write("\t"+line)
            keyval = line.split()
            if (len(keyval)>1):
                settings[keyval[0]] = keyval[1]
    
    #Load cutoffs
    cutoffs = {}
    cutoffsfile = open("/etc/sleepybox/cutoffs","r")
    statuslogfile.write("Cutoffs loaded:\n")
    for line in cutoffsfile:
        if (len(line.strip()) > 0 and line.strip()[0] !="#"):
         #statuslogfile.write("\t"+line)
         cutofftuple = line.split()
         if(len(cutofftuple)==5):
             try:
                 key = cutofftuple[0]
                 c = float(cutofftuple[1])
                 c2 = float(cutofftuple[2])
                 if(cutofftuple[3] == "r"):
                     r = True
                 elif (cutofftuple[3] == "s"):
                     r = False
                 else:
                     raise Exception()
                 if (cutofftuple[4] == "a"):
                    a = True
                 elif (cutofftuple[4] == "b"):
                    a = False
                 else:
                    raise Exception()
                 cutoffs[key] = {"suspendCutoff":c,"screenCutoff":c2,"rate":r,"actAbove":a}
                 statuslogfile.write("\t"+key +" : "+ str(cutoffs[key])+"\n")
             except:
                 statuslogfile.write("!!! Error loading cutoffs for module: "+cutofftuple[0])
                 modules.pop(cutofftuple[0],None)
    
    statuslogfile.flush()
    
    #Enter main loop    
    while(True):
        suspend = True
        screenblank = True
        
        #Check all the metrics
        for name,metricModule in modules.items():
            try:
                metric = metricModule.getMetric(int(settings['POLLTIME']))
                if(not cutoffs[name]["actAbove"] and metric > cutoffs[name]["suspendCutoff"]):
                    suspend = False
                if( cutoffs[name]["actAbove"] and metric < cutoffs[name]["suspendCutoff"]):
                    suspend = False
                if (not cutoffs[name]["actAbove"] and metric > cutoffs[name]["screenCutoff"]):
                    screenblank = False
                if (cutoffs[name]["actAbove"] and metric < cutoffs[name]["screenCutoff"]):
                    screenblank = False
                logfile.write( ("{0}: {1"+metricModule.getFormatting()+"} {2}; ").format(name,metric,metricModule.getUnits()))
            except:
                statuslogfile.write("!!! Error getting the metrics from module: "+name+"\n"+
                                    "Exception:\n")
                statuslogfile.write(traceback.format_exc())
                modules.pop(name)
                statuslogfile.flush()
        logfile.write("\n")
        logfile.flush()
        
        #Take action
        if (suspend):
            logfile.write("______________________Suspend Triggered_____________________\n")
            logfile.flush()
            dbusSession = dbus.SystemBus()
            proxy = dbusSession.get_object("org.freedesktop.UPower", "/org/freedesktop/UPower")
            #proxy.Suspend(dbus_interface="org.freedesktop.UPower")
        elif(screenblank):
            logfile.write("______________________Screen shutdown Triggered_____________________\n")
            logfile.flush()
            #subprocess.call("xset dpms force standby")
           
        time.sleep(int(settings['POLLTIME']))