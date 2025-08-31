from TTS.api import TTS
import soundfile as sf
from os import makedirs
import numpy as np
from torch import cuda
import random

class TTSModel:
    def __init__(self,output_dir = "voice_output"):
        # model init
        device = "cuda" if cuda.is_available() else "cpu"
        self.tts = TTS(model_name="tts_models/en/vctk/vits").to(device=device)
        
        # model configs
        # self.speaker = "ED\n" # the most natural one for our worklaod
        self.speaker = random.choice(self.tts.speakers)
        self.sample_rate = 22050
        
        # output configs
        self.output_dir = output_dir.strip()
        makedirs(output_dir, exist_ok=True)
        
    def GenerateAudio(self, text):

        wav = self.tts.tts(text, speaker=self.speaker)
        wav = np.array(wav, dtype=np.float32)

        return wav

    def SpeakAndSave(self, text, file_name):

        wav = self.tts.tts(text, speaker=self.speaker)
        wav = np.array(wav, dtype=np.float32)

        output_dest = self.output_dir + "/" + file_name.strip() + ".wav"
        sf.write(output_dest, wav, self.sample_rate)
        return output_dest

if __name__ == "__main__":
    tts = TTSModel("voice_test")
    tts.SpeakAndSave("this is a test","test1")
    tts.SpeakAndSave("this is a test","test2")