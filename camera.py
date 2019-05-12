import cv2
import threading
import pyaudio
import wave
import time
class RecordingThread (threading.Thread):
    def __init__(self, name, camera,candidate):
        threading.Thread.__init__(self)
        self.name = name
        self.isRunning = True

        self.cap = camera
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        filename="./static/{}.avi".format(candidate)
        self.out = cv2.VideoWriter(filename,fourcc, 20.0, (640,480))

    def run(self):
        while self.isRunning:
            ret, frame = self.cap.read()
            if ret:
                self.out.write(frame)

        self.out.release()

    def stop(self):
        self.isRunning = False

    def __del__(self):
        self.out.release()




class VoiceThread (threading.Thread):
    def __init__(self, name, camera,candidate):
        threading.Thread.__init__(self)
        self.name = name
        self.isRunning = True
        self.startTime=0;
        self.endTime=0;
        self.candidate=candidate
        self.audio = pyaudio.PyAudio()
        self.audioframes=None
        self.stream=None

    def run(self):
        #while self.isRunning:
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        CHUNK = 1024
        RECORD_SECONDS = 5000000
        filename="./static/{}.wav".format(self.candidate)
        WAVE_OUTPUT_FILENAME = filename
        self.startTime=time.time()
        # start Recording
        self.stream = self.audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
        print ("recording...")
        self.audioframes = []

        #recordTime=self.endTIme-self.startTime;
        #for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        while self.isRunning:
            data = self.stream.read(CHUNK)
            self.audioframes.append(data)

        self.endTime=time.time()

        print ("finished recording")
        # stop Recording
        k=self.stream
        k.stop_stream()
        k.close()
        self.audio.terminate()
        
        waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(self.audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(self.audioframes))
        waveFile.close()

    def stop(self):
        self.isRunning = False



class VideoCamera(object):
    def __init__(self):
        # Open a camera
        self.cap = cv2.VideoCapture(0)
      
        # Initialize video recording environment
        self.is_record = False
        self.out = None

        # Thread for recording
        self.recordingThread = None
        self.voiceThread = None
    
    def __del__(self):
        self.cap.release()
    
    def get_frame(self):
        ret, frame = self.cap.read()

        if ret:
            ret, jpeg = cv2.imencode('.jpg', frame)

            # Record video
            # if self.is_record:
            #     if self.out == None:
            #         fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            #         self.out = cv2.VideoWriter('./static/video.avi',fourcc, 20.0, (640,480))
                
            #     ret, frame = self.cap.read()
            #     if ret:
            #         self.out.write(frame)
            # else:
            #     if self.out != None:
            #         self.out.release()
            #         self.out = None  

            return jpeg.tobytes()
      
        else:
            return None

    def start_record(self,candidate): 
        self.is_record = True
        self.recordingThread = RecordingThread("Video Recording Thread", self.cap,candidate)
        self.voiceThread = VoiceThread("Video Recording Thread", self.cap,candidate)
        self.recordingThread.start()
        self.voiceThread.start()

    def stop_record(self,candidate):
        self.is_record = False

        if self.recordingThread != None:
            self.recordingThread.stop()
        if self.voiceThread != None:
            self.voiceThread.stop()

            