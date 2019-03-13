from pydub import AudioSegment
import numpy as np
#loading string data
sound = AudioSegment.from_mp3("C:/Dev/Guitar Tuner/GuitarTuner/Samples/1st_String_E_64kb.mp3")
data = np.fromstring(sound.raw_data, dtype=np.int16)
sr = sound.frame_rate
ss = sound.sample_width
channels = sound.channels

# FFT
fftData = np.FFT(data)
frames = channels * ss
time = frames / sr

print("Sound Rate: %d\nSample Width: %d\nChannels: %d\n" % sr, ss, channels)