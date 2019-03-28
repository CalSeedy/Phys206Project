#import globals (shared variables like current string and tuning set)
#import GPIO module
import sharedGlobals as sg
import pydub as pd
import numpy as np
import scipy.signal as sps
import matplotlib.pyplot as plt
import ListArrayforFrequencies as allNotes
import referenceFreqs, math, csv
from numpy.fft import fft,fftfreq

class Sound:
    data = []
    
    def __init__(self):
        self.listening = True

    def close(self):
        self.listening = False

    def getData(self):
        #take input from jack
        #self.data.append(inp)
        pass
    
    def run(self):
        while self.listening:
            #collect data
            self.getData()
            
            #transform data
            fftData = self.FFT(self.data)

            #analyse data (find peak and compare)
            self.analyse(fftData)

    def FFT(self, data):
        # Conner's fft code
        n = len(data)
        #cretaes all necessary frequencies
        freqs = fftfreq(n) * sg.rate
        #need mask array to get rid of half the values as they are the complex conjugate
        mask = np.where(np.logical_and(freqs >= 0, freqs <= 4000)) #lim_up = 4000Hz, lim_low = 0Hz
        #fft values
        fft_vals = fft(data)#self.data)
        #true theoretical fft
        fft_theo = 2.0*np.abs(fft_vals/n)

        #FFT Plot
        plt.figure(2)
        plt.plot(freqs[mask],fft_theo[mask],label='FFT Values')
        plt.title('FFT Values')
        plt.show(block=False)
        return freqs, fft_theo
    
    def analyse(self):
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
        freqs, fftData = self.FFT(data)

        #find max
        mx = freqs[np.argmax(fftData)]
        
        print("Maximum at: %f Hz" % (mx))


        nearest, f_nearest = getNearest(mx) 
        # freq to cents
        #c = 1200 * math.log2(f_max / f_ref)
        c = 1200 * math.log2(mx / f_nearest)
        print ("offset from closest: %f cents (note: %s)" % (c, nearest))

        sg.tuning = ["E2", "A2", "D3", "G3", "B3", "E4"] # standard tuning
        sg.string = 2 #1-6, 1 being lowest pitch 
        ind = sg.tuning[sg.string - 1]
        f_tuning = getFrequency(ind)
        a = 1200 * math.log2(mx / f_tuning)
        # +ve offset -> too sharp, -ve -> too flat
        print ("Detected note: %s | Target note: %s | Offset (cents): %f" % (nearest, ind, a) )

s = Sound()
s.analyse()