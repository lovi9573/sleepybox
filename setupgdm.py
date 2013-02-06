"""
Initial draft setup procedure to collect network interface and sound channel settings.
written by: Jesse Lovitt

"""

import subprocess
import stat
import os
from os.path import expanduser


def insertTxt(filepath, entry):
	#Add Per user session script hooks to gdm PreSession and PostSession
	PreFN = os.path.normpath(filepath)
	fh = open(PreFN, "r")
	default = fh.readlines()
	a = 0
	b = 0	
	end = -1
	for i,line in enumerate(default):
		if line[0:3] == "###":
			if line[4:7] == "Run":
				a = i
			elif line[4:7] == "End":
				b = i +1
		elif line[0:4] == "exit":
			end = i
	default = default[0:a] + default[b:end] + [entry] + default[end:]
##  Need elevated permissions.
	fh = open(PreFN, "w")
	fh.writelines(default)



if __name__ == "__main__":
	#Presesssion entry
	entry = """### Run Per User Session Scripts
  if [ -n "$HOME" ] && [ -n "$USER" ] && [ -d "$HOME/.session/" ]; then
    for script in "$HOME/.session"/* ; do
      if [ -f "$script" ]; then
        $script presession
      fi
    done
  fi
### End Per User Session Scripts
"""
	insertTxt("/etc/gdm/PreSession/Default",entry)
	
	#Postsession entry
	entry = """### Run Per User Session Scripts
  if [ -n "$HOME" ] && [ -n "$USER" ] && [ -d "$HOME/.session/" ]; then
    for script in "$HOME/.session"/* ; do
      if [ -f "$script" ]; then
        $script postsession
      fi
    done
  fi
### End Per User Session Scripts

"""
	insertTxt("/etc/gdm/PostSession/Default",entry)
	
	


