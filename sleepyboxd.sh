#/bin/bash
DIR="$( cd "$( dirname "$0" )" && pwd )"
DATE=$(date)
echo $$ > $DIR/pid
echo "" > $DIR/cansuspend.log
. $DIR/sleepyboxsettings.sh
echo "[POWERON]================="$DATE"=================" >> $DIR/cansuspend.log
CPUAVE=1000
NETAVE=30
AUDIOAVE=10
SCREENDIFFTIME=0
RX=$(ifconfig $NETCARD|grep 'RX packets'|cut -d' ' -f14)
TX=$(ifconfig $NETCARD|grep 'TX packets'|cut -d' ' -f14)
export DIR DATE CPUAVE NETAVE AUDIOAVE SCREENDIFFTIME RX TX
while [ -e $DIR/run ]
do 
  #Read settings (put here so settings can change while this script continues to run as daemon)
  . $DIR/sleepyboxsettings.sh
  #Chech for suspend criteria and suspend if needed
  . $DIR/cansuspend
  #Wait for next check
  sleep $SLEEPTIME
done
