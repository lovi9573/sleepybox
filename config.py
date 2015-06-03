import os


def getConfig(f):
	config = {}
	if os.path.isfile(f):
		with open(f,"r") as fin:
			for line in [x.strip() for x in fin]:
				if len(line) > 0 and line[0] != "#":
					i = line.index(" ")
					config[line[:i]] = line[i+1:]
	return config

def getModuleConfig(f):
	modules={}
	currentmodule = ''
	if os.path.isfile(f):
		with open(f,"r") as fin:
			for line in [x.strip() for x in fin]:
				if len(line)>0 and line[0] != "#":
					if line[0] == '[' and line[-1] == ']':
						currentmodule = line[1:-1]
						modules[currentmodule] = {}
					elif currentmodule != '':	
						key,val = line.split() 
						modules[currentmodule][key] = val
	return modules
	
