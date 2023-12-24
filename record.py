import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np

class Recorder:
    def __init__(self, samplerate=44100, channels=1):
        self.samplerate = samplerate
        self.channels = channels
        self.recorded_frames = []
        self.recording = False

    def start_recording(self):
        self.recording = True
        self.recorded_frames = []
        self.stream = sd.InputStream(samplerate=self.samplerate, channels=self.channels, callback=self.callback)
        self.stream.start()
        print("Recording...")

    def stop_recording(self):
        self.recording = False
        self.stream.stop()
        self.stream.close()
        record = np.concatenate(self.recorded_frames, axis=0)
        write("rec.wav", self.samplerate, record)
        print("Recording stopped and saved as 'rec.wav'.")

    def callback(self, indata, frames, time, status):
        if self.recording:
            self.recorded_frames.append(indata.copy())


