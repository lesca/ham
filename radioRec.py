# Record microphone input waves into wav file, cut off quiets automatically
# based on Joie_Yu's efforts on this website: https://my.oschina.net/u/3404800/blog/3017039

import threading
import pyaudio
import copy
import math
import time
import numpy
import wave


class RecordThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.localtime = time.localtime()
        self.localtimestr = time.strftime("%Y-%m-%d-%H-%M-%S",self.localtime)
        self.bRecord = True
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000
        self.srtFile = open('./remote/'+self.localtimestr+ '.srt','a+', encoding='utf-8')
        self.line = 1
        self.audiofile = "./remote/{}.wav".format(self.localtimestr)
        self.audio = pyaudio.PyAudio()
        self.wavfile = wave.open(self.audiofile, 'wb')
        self.wavfile.setnchannels(self.channels)
        self.wavfile.setsampwidth(self.audio.get_sample_size(self.format))
        self.wavfile.setframerate(self.rate)
        self.wavstream = self.audio.open(format=self.format,
                               channels=self.channels,
                               rate=self.rate,
                               input=True,
                               frames_per_buffer=self.chunk)
    def run(self):
        xx = 0
        yy = 0
        alltime = 0
        starttime = 0
        stoptime = 0
        timediff = 0

        # srt top center
        self.srt("{}\n0:00:00,000 --> 0:00:10,000\n{{\\an8}}<font color=#FFFF00>录制日期：{}</font>\n".format(str(rt.line),str(time.strftime("%Y-%m-%d",rt.localtime))))
        # srt mid center
        self.srt("{}\n0:00:00.000 --> 0:00:10.000\n{{\\an5}}请遵守<font color=#FF0000><u><b>《中华人民共和国无线电管理条例》</b></u></font>\n".format(str(rt.line)))
        print("RUN ...... Start at {}".format(rt.localtimestr))

        while self.bRecord:
            data = self.wavstream.read(self.chunk*5)
            wavdata = numpy.frombuffer(data,dtype=numpy.short)
            M = []
            M.append(wavdata)
            M=map(abslist,M)
            sound = list(map(mean,M))
            #print(sound)
            if sound[0] > 500:
                xx = 1
                self.wavfile.writeframes(data)
            else:
                xx = 0
            if xx > yy:
                yy = 1
                #START
                starttime = time.time()
                alltime = round(alltime + timediff,3)
                print("{:03d} StartTime: {} Timestamp: {}".format(
                    self.line, time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(starttime)), timestr(alltime)))
            if xx < yy:
                yy = 0
                #STOP
                stoptime = time.time()
                timediff = round(stoptime - starttime,3)
                
                self.srt("{}\n{} --> {}\n<font color=#5F9F9F>{}  ->  {}</font>\n<font color=#4D4DFF>{}</font>\n".format(
                    str(self.line),timestr(alltime),timestr(alltime+timediff),
                    time.strftime("%H:%M:%S",time.localtime(starttime)),time.strftime("%H:%M:%S",time.localtime(stoptime)),timestr(timediff)))
                self.line = self.line + 1
                print("    StopTime:  {} Timestamp: {}".format(
                    time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(stoptime)), timestr(alltime+timediff)))
                print("    Duration: {}\n".format(timestr(timediff)))
        # out of while loop - clean up
        self.wavstream.stop_stream()
        self.wavstream.close()
        self.audio.terminate()
        self.srtFile.close()

    # output msg to srt file
    def srt(self, msg):
        self.srtFile.write(msg+"\n")
        self.srtFile.flush()

def abslist(a):
    return list(map(abs,a))

def mean(a):
    return numpy.longlong(sum(a)) / len(a)

def timestr(sec):
    m,s = divmod(sec,60)
    h,m = divmod(m,60)
    return "{:02d}:{:02d}:{:02d},{:03d}".format(int(h),int(m),int(s),int((s-int(s))*1000))


# Main
if __name__ == '__main__':
    try:
        rt = RecordThread()
        rt.start()
        while True:
            time.sleep(60)
            localtime = time.localtime()
            if localtime.tm_hour == 00 and localtime.tm_min == 00:
                # Reload instance at midnight
                rt.bRecord = False
                rt = RecordThread()
                rt.start()
    except KeyboardInterrupt as e:
        print("Caught keyboard interrupt. Killing threads ...")
        rt.bRecord = False

