import numpy as np
import pyaudio
import webrtcvad
from collections import deque
import wave

class StreamPatcher:
    def __init__(self):
        self.format = pyaudio.paInt16
        self.ch = 1
        self.rate = 16000
        self.chunk_time = 30
        self.chunk_size = self.rate * self.chunk_time // 1000
        self.window_chunk = 15

        self.th_start=0.8
        self.th_end=0.2

        self.p = pyaudio.PyAudio()
        self.vad = webrtcvad.Vad(1)

    def __enter__(self):
        self.stream = self.p.open(format=self.format,
                                  channels=self.ch,
                                  rate=self.rate,
                                  input=True,
                                  start=False,
                                  frames_per_buffer=self.chunk_size)
        self.stream.start_stream()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stream.stop_stream()
        self.stream.close()

    def __iter__(self):
        self.chunk_buffer=deque(maxlen=self.window_chunk)
        self.active_buffer=deque(maxlen=self.window_chunk)

        self.rec_buffer=[]
        self.start_rec=False

        return self

    def check_end(self):
        return sum(self.active_buffer)/self.window_chunk < self.th_end

    def check_start(self):
        return sum(self.active_buffer)/self.window_chunk > self.th_start

    def __next__(self):
        chunk = self.stream.read(self.chunk_size)
        active = self.vad.is_speech(chunk, self.rate)

        self.chunk_buffer.append(chunk)
        self.active_buffer.append(active)

        if self.start_rec:
            self.rec_buffer.append(chunk)
            if self.check_end():
                self.rec_data=np.hstack(self.rec_buffer)
                raise StopIteration
        else:
            if self.check_start():
                self.rec_buffer.extend(self.chunk_buffer)
                self.start_rec=True
        return chunk

if __name__ == '__main__':
    with StreamPatcher() as sp:
        for i in iter(sp):
            pass
        wf = wave.open('test.wav', 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(sp.p.get_sample_size(sp.format))
        wf.setframerate(sp.rate)
        wf.writeframes(b''.join(sp.rec_buffer))
        wf.close()