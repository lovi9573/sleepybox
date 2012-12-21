#####Settings for cansuspend script#####
#Inactivity time in seconds to trigger suspend (seconds)
IDLETIMEOUT=600
#Cpu use lower limit to trigger suspend (tenths of percent , 1000 is max)(140 for pandora)
CPULOWLIMIT=400
#Network lower limit to trigger suspend (kB/s) 
NETLOWLIMIT=20
#Weight given to new readings in the moving average (percent)
NEWREADINGWEIGHT=40
#Difference in screenshots lower limit (n pixels)
SCREENDIFFLIMIT=200000
#Sound output lower limit (??? units)
AUDIOLOWLIMIT=2
#Number of seconds to sleep before recheck for suspend criteria
SLEEPTIME=60

export IDLETIMEOUT CPULOWLIMIT NETLOWLIMIT NEWREADINGWEIGHT SCREENDIFFLIMIT AUDIOLOWLIMIT SLEEPTIME
