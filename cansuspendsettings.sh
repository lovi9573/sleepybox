#####Settings for cansuspend script#####
#Inactivity time in seconds to trigger suspend (seconds)
IDLETIMEOUT=600
#Cpu use lower limit to trigger suspend (tenths of percent , 1000 is max)(140 for pandora)
CPULOWLIMIT=400
#Network lower limit to trigger suspend (kB/s) 
NETLOWLIMIT=20
#Difference in screenshots lower limit (percent)
SCREENDIFFLIMIT=10
#Sound output lower limit (tenths of percent , 1000 is max)
AUDIOLOWLIMIT=2



#Number of seconds to sleep before recheck for suspend criteria
SLEEPTIME=6
#Weight given to new readings in the moving average (percent)
NEWREADINGWEIGHT=40
#Pixel area to resize screenshots to
SCREENAREA=500000
#Network card to read data throughput from
NETCARD=em1
#Audio Source to read from
SOUNDCARD=alsa_output.pci-0000_00_1b.0.analog-stereo.monitor

export IDLETIMEOUT CPULOWLIMIT NETLOWLIMIT NEWREADINGWEIGHT SCREENDIFFLIMIT AUDIOLOWLIMIT SLEEPTIME
