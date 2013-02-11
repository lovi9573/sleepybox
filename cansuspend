#/bin/bash

 #Gather metrics
 #Idle time
 IDLETIME=$(python $DIR/idletime.py)
 #Cpu usage
 CPU=$(top -b -n 2 -d 0.5 | grep "Cpu(s)" | tail -n 1 | sed "s/.*, *\([0-9.]*\)%\id.*/\1/" | awk '{print 1000 - 10*$1}')
 #Network usage
 NR=$(ifconfig $NETCARD|grep 'RX packets'|cut -d' ' -f14)
 NT=$(ifconfig $NETCARD|grep 'TX packets'|cut -d' ' -f14)
 DR=$((NR - RX))
 DT=$((NT - TX))
 RX=$(ifconfig $NETCARD|grep 'RX packets'|cut -d' ' -f14)
 TX=$(ifconfig $NETCARD|grep 'TX packets'|cut -d' ' -f14)
 if [ $DR -gt $DT ]
 then 
	NET=$((DR/1000))
 else
	NET=$((DT/1000))
 fi
 #rotate screenshots, and get screenshot diff
 mv -f $DIR/screen0.png $DIR/screen1.png
 scrot $DIR/screen0.png
 mogrify -resize $SCREENAREA@ $DIR/screen0.png
 SCREENDIFF=$(compare -metric AE $DIR/screen0.png $DIR/screen1.png null: 2>&1)
 printf -v SCREENDIFF "%.f" "$SCREENDIFF"
 SCRDIFFPERCENT=$((SCREENDIFF*100/SCREENAREA))
 #Sample audio output and determine volume
 TMP=$(parec -d $SOUNDCARD |sox -t raw -r 44100 -sLb 16 -c 2 - -n trim 0 1 stat 2>&1 |grep RMS |grep amplitude)
 AUDIOVOLUME=$(echo $TMP |sed "s/[^0-9]*//" |awk '{printf("%d\n", $1*1000)}')
 if [ -z "$AUDIOVOLUME" ]; then
   AUDIOVOLUME=0
 fi

 #Get running averages
 NEWREADINGWEIGHT=$(echo '' | awk '{printf("%d\n",100*(1-0.1^('$SLEEPTIME'/'$DECAYTIME')))}')
 CPUAVE=$((($NEWREADINGWEIGHT*$CPU + (100-$NEWREADINGWEIGHT)* $CPUAVE)/100))
 NETAVE=$((($NEWREADINGWEIGHT*$NET + (100-$NEWREADINGWEIGHT)* $NETAVE)/100))
 AUDIOAVE=$((($NEWREADINGWEIGHT*$AUDIOVOLUME + (100-$NEWREADINGWEIGHT)* $AUDIOAVE)/100))
 TIMESTAMP=$(date +%x\ %X)

 ### Determine if criteria for shutdown are met.

 if [ $CPUAVE -lt $CPULOWLIMIT ] && [ $IDLETIME -gt $IDLETIMEOUT ] && [ $((NETAVE/SLEEPTIME)) -lt $NETLOWLIMIT ] && [ $SCRDIFFPERCENT -lt $SCREENDIFFLIMIT ] && [ $AUDIOAVE -lt $AUDIOLOWLIMIT ]
 then
	echo "["$TIMESTAMP"]-------Suspending due to inactivity and low cpu usage [ "$IDLETIME" : "$((CPUAVE/10))" : "$NETAVE" : "$SCRDIFFPERCENT" : "$AUDIOAVE" ]" >> $DIR/cansuspend.log
	ps au -U 500 | sed -r 's/(.*)/\t\1/' >> $DIR/cansuspend.log
	echo "" >> $DIR/cansuspend.log
	if [ -n "$VBMACHINE" ]; then
	  for MACH in "${VBMACHINE[*]}" 
	  do
	    VBoxManage controlvm $MACH savestate &> $DIR/cansuspenderror.log
	  done
	fi	
	dbus-send --system --print-reply --dest="org.freedesktop.UPower" /org/freedesktop/UPower org.freedesktop.UPower.Suspend &
 else
	echo "["$TIMESTAMP"] "$IDLETIME" s : "$((CPUAVE/10))" % ("$((CPU/10))") : "$((NETAVE/SLEEPTIME))" kB/s ("$((NET/SLEEPTIME))") : "$SCREENDIFF" px ("$SCRDIFFPERCENT"%) : "$AUDIOAVE" 1000ths ("$AUDIOVOLUME") : "$NEWREADINGWEIGHT" wght" >> $DIR/cansuspend.log
	if [ $SCRDIFFPERCENT -lt $SCREENDIFFLIMIT ]
	then
		SCREENDIFFTIME=$(($SCREENDIFFTIME+$SLEEPTIME))		
		if [ $SCREENDIFFTIME -gt $MONITORTIMEOUT ] && [ $IDLETIME -gt $IDLETIMEOUT ]
   		then
			echo " dpms suspend" >> $DIR/cansuspend.log
			SCREENDIFFTIME=0
			xset dpms force standby
		fi
	fi
 fi


	   




