
def getConfig(f):
	config = {}
	with open(f,"r") as fin:
		for line in fin:
			if line.strip()[0] != "#":
				i = line.indexof(" ")
				config[line[:i]] = line[i+1:]
	return config

def getCutoffs(f):
	cutoffs={}
	with open(f,"r") as fin:
		for line in fin:
			if line.strip()[0] != "#":
				name,c1,c2,t,ab = line.split(" ")
				cutoffs[name] = {}
				cutoffs[name]['sleepcut'] = int(c1)
				cutoffs[name]['screencut'] = int(c2)
				cutoffs[name]['type'] = t
				cutoffs[name]['a/b'] = ab
	return cutoffs
	
