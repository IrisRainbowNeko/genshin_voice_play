import wave
import numpy as np
from .stream_patch import StreamPatcher

class SpeechRecognizer:
    def __init__(self, context=('丘丘人', '雷史莱姆', '变异雷史莱姆', '雷莹术士', '盗宝团', '火之债务处理人', '冰史莱姆',
           '冰深渊法师', '岩龙蜥', '雷岩龙蜥', '火史莱姆', '大丘丘人', '火深渊法师', '雷丘丘王', '雷深渊法师', '攻击', '战术')):
        import wenet
        self.decoder = wenet.Decoder(lang='chs', context=context, context_score=10.0)
        self.first=True

    def next(self, chunk_wav):
        ans = self.decoder.decode(chunk_wav)
        self.decoder.reset()
        ans = eval(ans)
        ans = ans['nbest'][0]['sentence'].replace('<context>','').replace('</context>','')
        return ans

    def test_file(self, file):
        ans = self.decoder.decode_wav(file)
        self.decoder.reset()
        ans = eval(ans)
        ans = ans['nbest'][0]['sentence'].replace('<context>','').replace('</context>','')
        return ans


if __name__ == '__main__':
    with StreamPatcher() as sp:
        sr = SpeechRecognizer()
        sr.test_file('../data/voice_test.wav')
        while True:
            print('start')
            for i in iter(sp):
                pass
            print('rec')
            text = sr.next(sp.rec_data.tobytes())
            print(text)


