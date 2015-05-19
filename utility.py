import glob
import re
import subprocess
import re


def getXSessions():

    files = glob.glob("/tmp/.X*-lock")
    displays = []
    r = re.compile('/tmp/.X(\d)*-lock')
    for file in files:
        m = r.match(file)
        displays.append(int(m.group(1)))
    return displays

def getXSessionAuths():
    """
    TODO
    get Xsessions and users mapped together from 'who'
    dump a listing of /run/gdm/ into a list
    for each user find the dir that matches "auth-for-USER-*" and append a /database to it.
    Return the dictionary {user :  [display, authfile]}
    """
    authDirs = glob.glob("/run/gdm/auth-for-*")
    whoListing = subprocess.check_output(["who"])
    who = {}
    for line in whoListing.split("\n"):
        cols = line.split()
        #if it is an X display login
        if (len(cols) > 1 and cols[1][0] == ":"):
            #find Xauthority file
            authDir = ""
            authDirsIter = iter(authDirs)
            try:
                while (not re.match("/run/gdm/auth-for-"+cols[0]+"-" , authDir) ):
                    authDir = authDirsIter.next()
            except :
                pass
                
            if (authDir != ""):
                #Enter in dictionary
                who[cols[0]] = {"display": cols[1], "xauthority": authDir+"/database"}
    return who
            
            
            
            