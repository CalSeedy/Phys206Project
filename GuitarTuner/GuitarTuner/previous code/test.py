import pydub as pd
import numpy as np
import scipy.signal as sps
import matplotlib.pyplot as plt
import referenceFreqs, math, csv
import ListArrayforFrequencies as allNotes


def getFrequency(note):
    with open("frequencies.csv", "r") as readFile:
        out = -1
        reader = csv.reader(readFile)
        for row in readFile:
            row = row.split(",")
            row[1] = float(row[1])
            if row[0] == note:
                out = row[1]
        readFile.close()
    if out != -1:
        return out
    else:
        raise Exception("Note (%s) not found in database!" % (note))
        

def getNearest(frequency):
    closest = []
    pairs = []
    with open("frequencies.csv", "r") as readFile:
        reader = csv.reader(readFile)
        for row in readFile:
            row = row.split(",")
            row[1] = float(row[1])
            pairs.append([row[0], row[1]])
        readFile.close()
    dif = []
    for i in pairs:
        dif.append(abs(i[1] - frequency))
    closest = pairs[dif.index(min(dif))]
    note = closest[0]
    freq = closest[1]
    return note, freq


# loading sound data                    
sound = pd.AudioSegment.from_mp3("../Samples/5th_String_A_64kb.mp3")
data = np.fromstring(sound.raw_data, dtype=np.int16)
sr = sound.frame_rate
ss = sound.sample_width
channels = sound.channels

# FFT
fftAmp = np.fft.fft(data)
fftFreqs = np.fft.fftfreq(len(data))
time = len(data) / sr
fftAmp = np.abs(fftAmp)
#fftFreqs = fftFreqs >= 0

#print(fftFreqs.min() * sr, fftFreqs.max() * sr)

freq_in_hertz = abs(fftFreqs * sr)
#print(freq_in_hertz)
#print("Sound Rate: %d\nSample Width: %d\nChannels: %d\nTotal time: %f secs\n" % (sr, ss, channels, time))

#find max
freq = fftFreqs[np.argmax(np.abs(fftAmp))]
mx = abs(freq * sr)
print("Maximum at: %f Hz" % (mx))

t = []
delta = 1/sr
for i in range(len(data)):
    if i == 0:
        t.append(0)
    else:
        t.append(t[i-1] + delta)

plt.plot(freq_in_hertz, np.abs(fftAmp), 'b')
plt.show(block=False)


nearest, f_nearest = getNearest(mx)

tuning = ["E2", "A2", "D3", "G3", "B3", "E4"]
currentString = 2 #1-6, 1 being lowest pitch  
# freq to cents
#c = 1200 * math.log2(f_max / f_ref)
c = 1200 * math.log2(mx / f_nearest)
print ("offset from closest: %f cents (note: %s)" % (c, nearest))


ind = tuning[currentString - 1]
f_tuning = getFrequency(ind)
a = 1200 * math.log2(mx / f_tuning)
# +ve offset -> too sharp, -ve -> too flat
print ("Detected note: %s | Target note: %s | Offset (cents): %f" % (nearest, ind, a) )
