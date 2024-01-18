import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np

class Recorder:
    def __init__(self, samplerate=44100, channels=1, silence_threshold=0.01, silence_duration=2):
        self.samplerate = samplerate
        self.channels = channels
        self.silence_threshold = silence_threshold
        self.silence_duration = silence_duration
        self.recorded_frames = []
        self.recording = False
        self.silence_counter = 0

    def start_recording(self):
        self.recording = True
        self.recorded_frames = []
        self.silence_counter = 0
        self.stream = sd.InputStream(samplerate=self.samplerate, channels=self.channels, callback=self.callback)
        self.stream.start()
        print("Recording...")

    def stop_recording(self):
        self.recording = False
        self.stream.stop()
        self.stream.close()
        record = np.concatenate(self.recorded_frames, axis=0)
        write("./audio/rec.wav", self.samplerate, record)
        print("Recording stopped and saved as 'rec.wav'.")

    def callback(self, indata, frames, time, status):
        if status:
            print(status)

        if self.recording:
            self.recorded_frames.append(indata.copy())
            if np.abs(indata).mean() < self.silence_threshold:
                self.silence_counter += 1
                if self.silence_counter >= self.silence_duration * self.samplerate / frames:
                    self.stop_recording()
            else:
                self.silence_counter = 0
