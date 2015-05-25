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

def getCutoffs(f):
	cutoffs={}
	if os.path.isfile(f):
		with open(f,"r") as fin:
			for line in [x.strip() for x in fin]:
				if len(line)>0 and line[0] != "#":
					name,c1,c2,t,ab = line.split(" ")
					cutoffs[name] = {}
					cutoffs[name]['sleepcut'] = float(c1)
					cutoffs[name]['screencut'] = float(c2)
					cutoffs[name]['type'] = t
					cutoffs[name]['a/b'] = ab
	return cutoffs
	
