
/*
# h2xml.py -I $PWD -c -o pa.xml pulse/mainloop-api.h pulse/sample.h pulse/def.h pulse/operation.h pulse/context.h pulse/channelmap.h pulse/volume.h pulse/stream.h pulse/introspect.h pulse/subscribe.h pulse/scache.h pulse/version.h pulse/error.h pulse/xmalloc.h pulse/utf8.h pulse/thread-mainloop.h pulse/mainloop.h pulse/mainloop-signal.h pulse/util.h pulse/timeval.h
# xml2py.py -k efstd -o lib_pulseaudio.py -l 'pulse' -r '(pa|PA)_.+' pa.xml
from ctypes import *
_libraries = {}
_libraries['libpulse.so.0'] = CDLL('libpulse.so.0')
*/
#include <stdlib.h>
#include <sample.h>
#include <simple.h>

#define BUFSIZE 22050

int getPeak(char* sink){
	pa_simple *s;
	pa_sample_spec ss;
	ss.format = PA_SAMPLE_S16NE;
	ss.channels = 2;
	ss.rate = 44100;
	s = pa_simple_new(	NULL,// Use the default server.
						"Fooapp", // Our application's name.
						PA_STREAM_PLAYBACK,
						NULL, // Use the default device.
						"Music", // Description of our stream.
						&ss, // Our sample format.
						NULL, // Use default channel map
						NULL, // Use default buffering attributes.
						NULL // Ignore error code.
						);
	int16_t data[BUFSIZE];
	pa_simple_read(s,data,sizeof(data)/2,NULL);
	int16_t maxl = 0;
	int16_t maxr = 0;
	int i;
	for(i=0; i < sizeof(data)/2; i++){
		maxl = MAX(maxl, abs(data[2*i]));
		maxr = MAX(maxr, abs(data[2*i+1]));
	}
	pa_simple_free(s);
	return MAX(maxl, maxr);
}

void main(int argc, char* argv[]){
	char* sink = "some sink";
	getPeak(sink);
}

/*
class Metric(suspendmetric.suspendmetric):

    def __init__(self):
        #TODO: get this from the setup script
        self.sink_name = "alsa_output.pci-0000_00_1b.0.analog-stereo"
        self._context_notify_cb = pa_context_notify_cb_t(self.context_notify_cb)
        self._sink_info_cb = pa_sink_info_cb_t(self.sink_info_cb)
        self._stream_read_cb = pa_stream_request_cb_t(self.stream_read_cb)

        # stream_read_cb() puts peak samples into this Queue instance
        self._samples = Queue()



    def getSample(self,x):
       # Create the mainloop thread and set our context_notify_cb
        # method to be called when there's updates relating to the
        # connection to Pulseaudio
        _mainloop = pa_threaded_mainloop_new()
        _mainloop_api = pa_threaded_mainloop_get_api(_mainloop)
        context = pa_context_new(_mainloop_api, 'peak_demo')
        pa_context_set_state_callback(context, self._context_notify_cb, None)
        pa_context_connect(context, None, 0, None)
        pa_threaded_mainloop_start(_mainloop)


    def getUnits(self):
       return "/1"

    def getFormatting(self):
       return ":<4.2"

    def context_notify_cb(self, context, _):
        state = pa_context_get_state(context)

        if state == PA_CONTEXT_READY:
            print "Pulseaudio connection ready..."
            # Connected to Pulseaudio. Now request that sink_info_cb
            # be called with information about the available sinks.
            o = pa_context_get_sink_info_list(context, self._sink_info_cb, None)
            pa_operation_unref(o)

        elif state == PA_CONTEXT_FAILED :
            print "Connection failed"

        elif state == PA_CONTEXT_TERMINATED:
            print "Connection terminated"

    def sink_info_cb(self, context, sink_info_p, _, __):
        if not sink_info_p:
            return

        sink_info = sink_info_p.contents
        print '-'* 60
        print 'index:', sink_info.index
        print 'name:', sink_info.name
        print 'description:', sink_info.description

        if sink_info.name == self.sink_name:
            # Found the sink we want to monitor for peak levels.
            # Tell PA to call stream_read_cb with peak samples.
            print
            print 'setting up peak recording using', sink_info.monitor_source_name
            print
            samplespec = pa_sample_spec()
            samplespec.channels = 1
            samplespec.format = PA_SAMPLE_U8
            samplespec.rate = self.rate

            pa_stream = pa_stream_new(context, "peak detect demo", samplespec, None)
            pa_stream_set_read_callback(pa_stream,
                                        self._stream_read_cb,
                                        sink_info.index)
            pa_stream_connect_record(pa_stream,
                                     sink_info.monitor_source_name,
                                     None,
                                     PA_STREAM_PEAK_DETECT)

    def stream_read_cb(self, stream, length, index_incr):
        data = c_void_p()
        pa_stream_peek(stream, data, c_ulong(length))
        data = cast(data, POINTER(c_ubyte))
        for i in xrange(length):
            # When PA_SAMPLE_U8 is used, samples values range from 128
            # to 255 because the underlying audio data is signed but
            # it doesn't make sense to return signed peaks.
            self._samples.put(data[i] - 128)
        pa_stream_drop(stream)
*/
