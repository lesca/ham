# Record microphone input waves into wav file, cut off quiets automatically
# based on Joie_Yu's efforts on this website: https://my.oschina.net/u/3404800/blog/3017039

import threading
import pyaudio
import copy
import math
import time
import numpy
import wave

localtime = time.localtime()
localtimestr = time.strftime("%Y-%m-%d-%H-%M-%S",localtime)
#ltime = time.time()
line = 0
class RecordThread(threading.Thread):
    def __init__(self, audiofile="./remote/"+localtimestr+".wav"):
        threading.Thread.__init__(self)
        self.bRecord = True
        self.rr = True
        self.audiofile = audiofile
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000

    def run(self):
        #print("RUN....")
        audio = pyaudio.PyAudio()
        wavfile = wave.open(self.audiofile, 'wb')
        wavfile.setnchannels(self.channels)
        wavfile.setsampwidth(audio.get_sample_size(self.format))
        wavfile.setframerate(self.rate)
        wavstream = audio.open(format=self.format,
                               channels=self.channels,
                               rate=self.rate,
                               input=True,
                               frames_per_buffer=self.chunk)
        global xx
        global yy
        xx = 0
        yy = 0
        global line
        alltime = 0
        ntime1 = 0
        ntime2 = 0
        starttime = 0
        stoptime = 0
        timediff = 0
        while self.bRecord:
            data = wavstream.read(self.chunk*5)
            wavdata = numpy.fromstring(data,dtype=numpy.short)
            M = []
            M.append(wavdata)
            M=map(abslist,M)
            sound = list(map(mean,M))
            #print(sound)
            if sound[0] > 500:
                xx = 1
                wavfile.writeframes(data)
            else:
                xx = 0
            if xx > yy:
                yy = 1
                #START
                starttime = time.time()
                alltime = round(alltime + timediff,3)
                
                log("StartTime: "+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(starttime))+"    开始时间: "+timestr(alltime))
                print("StartTime: "+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(starttime))+"    开始时间: "+timestr(alltime))
            if xx < yy:
                yy = 0
                #STOP
                stoptime = time.time()
                timediff = round(stoptime - starttime,3)
                
                srt(str(line)+"\n"+timestr(alltime)+" --> "+timestr(alltime+timediff)+"\n"+"<font color=#5F9F9F>"+time.strftime("%H:%M:%S",time.localtime(starttime))+"  ->  "+time.strftime("%H:%M:%S",time.localtime(stoptime))+"</font> "+"\n"+"<font color=#4D4DFF>"+timestr(timediff)+"</font>"+"\n")
                line = line + 1
                log("StopTime:  "+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(stoptime))+"    结束时间: "+timestr(alltime+timediff)+"\n")
                print("StopTime:  "+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(stoptime))+"    结束时间: "+timestr(alltime+timediff))
                print("时长: "+timestr(timediff)+"\n")
                 
        wavstream.stop_stream()
        wavstream.close()
        audio.terminate()
        
    def stoprecord(self):
        print("stop")
        self.bRecord = False
        
    def pause(self):
        print("pause")
        self.rr = False
       
    def next(self):
        print("next")
        self.rr = True
        
def abslist(a):
    return list(map(abs,a))
def mean(a):
    return numpy.longlong(sum(a)) / len(a)

def log(msg):
    with open('./remote/'+localtimestr+ '.txt','a+') as file:
        file.write(msg+"\n")
        file.close()

def srt(msg):
    with open('./remote/'+localtimestr+ '.srt','a+') as file:
        file.write(msg+"\n")
        file.close()

        
def timestr(sec):
    m,s = divmod(sec,60)
    h,m = divmod(m,60)
    return "{:02d}:{:02d}:{:02d},{:03d}".format(int(h),int(m),int(s),int((s-int(s))*1000))
    
rt = RecordThread()
line = line + 1

log("RUN ...... Start At "+localtimestr+"    SYS OK!"+"  Frequency:433.090Mhz")
print("RUN ...... Start At "+localtimestr+"    SYS OK!"+"  Frequency:433.090Mhz")
rt.start()
