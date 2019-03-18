import pydub as pd
import numpy as np
import matplotlib.pyplot as plt
import referenceFreqs, math


def getNotes(tuning):
    all = ["A", "A#/Bb", "B", "C","C#/Db", "D", "D#/Eb", "E", "F", "F#/Gb", "G", "G#/Ab"]
    

def getNearest(frequency: float, tuning: str):
    notes = getNotes(tuning)
    dif = [abs(x - frequency) for x in tuning]
    print(dif)
    f = min(dif)
    ind = dif.index(f)
    return (ind, notes[ind])


# loading sound data
sound = pd.AudioSegment.from_mp3("../Samples/1st_String_E_64kb.mp3")
data = np.fromstring(sound.raw_data, dtype=np.int16)
sr = sound.frame_rate
ss = sound.sample_width
channels = sound.channels

# FFT
fftAmp = np.fft.fft(data)
fftFreqs = np.fft.fftfreq(len(data))
time = len(data) / sr

print(fftFreqs.min(), fftFreqs.max())

freq_in_hertz = abs(fftFreqs * sr)
print(freq_in_hertz)
print("Sound Rate: %d\nSample Width: %d\nChannels: %d\nTotal time: %f secs\n" % (sr, ss, channels, time))




t = []
delta = 1/sr
for i in range(len(data)):
    if i == 0:
        t.append(0)
    else:
        t.append(t[i-1] + delta)

plt.plot(freq_in_hertz, np.abs(fftAmp), 'r-')
plt.show()

#find max
idx = np.argmax(np.abs(fftAmp))
freq = fftFreqs[idx]
mx = abs(freq * sr)
print("Maximum at: %f Hz" % (mx))


tuning = referenceFreqs.getFreqs("standard")
nearest = getNearest(mx, tuning)
f_nearest = tuning[nearest[0]]
# freq to cents
#c = 1200 * math.log2(f_max / f_nearest)
c = 1200 * math.log2(mx / f_nearest)
print ("offset: %d cents (Nearest: %s)" % (c, nearest[1]) )
