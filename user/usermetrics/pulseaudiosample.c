
/*
# h2xml.py -I $PWD -c -o pa.xml pulse/mainloop-api.h pulse/sample.h pulse/def.h pulse/operation.h pulse/context.h pulse/channelmap.h pulse/volume.h pulse/stream.h pulse/introspect.h pulse/subscribe.h pulse/scache.h pulse/version.h pulse/error.h pulse/xmalloc.h pulse/utf8.h pulse/thread-mainloop.h pulse/mainloop.h pulse/mainloop-signal.h pulse/util.h pulse/timeval.h
# xml2py.py -k efstd -o lib_pulseaudio.py -l 'pulse' -r '(pa|PA)_.+' pa.xml
from ctypes import *
_libraries = {}
_libraries['libpulse.so.0'] = CDLL('libpulse.so.0')
*/
#include <stdlib.h>
#include <stdio.h>
#include <sample.h>
#include <simple.h>

#define BUFSIZE 22050

float getPeak(char* sink){
	pa_simple *s;
	pa_sample_spec ss;
	ss.format = PA_SAMPLE_S16NE;
	ss.channels = 2;
	ss.rate = 44100;
	s = pa_simple_new(	NULL,// Use the default server.
						"Sleepybox", // Our application's name.
						PA_STREAM_RECORD,
						sink, // Use the default device.
						"SoundSample", // Description of our stream.
						&ss, // Our sample format.
						NULL, // Use default channel map
						NULL, // Use default buffering attributes.
						NULL // Ignore error code.
						);
	if(!s){
		return -1;
	}
	int16_t data[BUFSIZE];
	if(pa_simple_read(s,data,sizeof(int16_t)*BUFSIZE,NULL)<0){
		return -2;
	}
	int16_t maxl = 0;
	int16_t maxr = 0;
	int i;
	for(i=0; i < BUFSIZE/2; i++){
		//printf("%d\n",data[2*i]);
		maxl = MAX(maxl, abs(data[2*i]));
		maxr = MAX(maxr, abs(data[2*i+1]));
	}
	pa_simple_free(s);
	return ((float)MAX(maxl, maxr))/((1 << 16) -1);
}

/* void main(int argc, char* argv[]){
	char* sink = "some sink";
	while(1){
		printf("%d\n",getPeak(sink));
	}
}
*/

