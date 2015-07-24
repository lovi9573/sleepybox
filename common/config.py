import os


def getConfig(f):
	config = {}
	if os.path.isfile(f):
		with open(f,"r") as fin:
			for line in [x.strip() for x in fin]:
				if len(line.strip()) > 0 and line.strip()[0] != "#":
					try:
						key,val = line.strip().split()
						config[key] = val
					except:
						print "Error: Config file {} malformed on line {}".format(f,line)
	else:
		print "Error: Config file {} does not exist".format(f)
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
						try:
							key,val = line.split() 
							modules[currentmodule][key] = val
						except:
							print "Error: config file {} malformed on line {}\n".format(f,line)
					else:
						print "Error: Key-value pair {} in file {}is not in a [<module>] section".format(line,f)
	else:
		print "Error: Config file {} does not exist".format(f)
	return modules
	
