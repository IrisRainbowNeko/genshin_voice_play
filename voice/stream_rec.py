import wave
import wenet
import numpy as np
from stream_patch import StreamPatcher

class SpeechRecognizer:
    def __init__(self, context=('丘丘人','雷史莱姆')):
        self.decoder = wenet.Decoder(lang='chs', context=context)

    def next(self, chunk_wav):
        ans = self.decoder.decode(chunk_wav)
        return ans


if __name__ == '__main__':
    with StreamPatcher() as sp:
        sr = SpeechRecognizer()
        print('start')
        for i in iter(sp):
            pass

        text = sr.next(sp.rec_data.tobytes())
        print(text)


