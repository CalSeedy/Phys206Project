#import necessary files and modules
import RPi.GPIO as GPIO
import sharedGlobals as sg
#import pydub as pd
import numpy as np
import scipy.signal as sps
import matplotlib.pyplot as plt
import math, csv, serial, time
from numpy.fft import fft, fftfreq

#create a soudn class that controls anything to do with the sound input and output, including intermediate steps (i.e. analysis and transformation)
class Sound():
    #create variables for storing the sound data, USB serial and initialisation state
    data = []
    ser = 0
    initialised = False

    #init function sets the USB serial and sets the initialisation to true
    def init(self):
        self.ser = serial.Serial("/dev/ttyACM0", sg.rate)
        self.initialised = True

    #getData checks the serial for any incoming data and builds a buffer of 1024 values before setting the shared data variable to this buffer
    def getData(self):
        data = []
        i = 0
        self.ser.reset_input_buffer()
        while len(data) < 1024:
            if self.ser.inWaiting() > 0: 
                read = self.ser.readline()

                #take byte data, decode it into a string, then get rid of trailing whitespaces
                value = float(read.decode().rstrip())
                data.append(value)
        sg.data = data 
        
    #run function controls the main cycle for the sound analysis and sets the loop: collect -> transform -> analyse -> collect...
    def run(self):
        #if we havent set up everything, do so
        if not self.initialised:
            self.init()

        #while we want to be analysing data; collect the data, transform the data and analyse the data
        while sg.running:
            #print("Sound thread: running ")
            time.sleep(0.1)
            #collect data
            #self.getData()
            
            #transform data
            #fftData = self.FFT(self.data)

            #analyse data (find peak and compare)
            #self.analyse(fftData)
    #FFT function takes some array of data and uses the fast fourier transform method to convert data in the time domain to frequency domain.
    #it then returns the set of frequencies and the amplitudes at those frequencies as 2 different arrays
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
##        #FFT Plot
##        t = []
##        for i in range(len(data)):
##            t.append(i / sg.rate)
##        plt.figure(1)
##        plt.plot(t, data, label='Original Values')
##        plt.title('Original Values')
##        plt.show(block=False)
        
##        plt.figure(2)
##        plt.plot(freqs[mask],fft_theo[mask],label='FFT Values')
##        plt.title('FFT Values')
##        plt.show(block=False)
        return freqs, fft_theo
    
    #analyse function takes the shared data, finds the frequency of the largest peak, compares this maximum to the database of known frequencies (as well as the intended note)
    #and returns how close, in cents, the detected note is away from the expected value. Then, with that value, it activates one of the LEDs depending on the offset. 
    def analyse(self):
        
        #getFrequency function takes a note, i.e. A#5, and scans the database for the corresponding frequency, then returns that frequency
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

        #getNearest function takes in some frequency, i.e. 643.346 Hz, and finds the difference between that value and all the values in the database,
        #the note with smallest difference is the closest. The corresponding note and frequency is then returned.  
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
            
            #for every note, calculate the difference between its frequency and the argument frequency and add it to the dif array
            for i in pairs:
                dif.append(abs(i[1] - frequency))
                
            #assign the closest note, frequency pair to be the index of dif, where the value of dif is the minimum.
            closest = pairs[dif.index(min(dif))]
            note = closest[0]
            freq = closest[1]
            return note, freq

##        # loading sound data                    
##        sound = pd.AudioSegment.from_mp3("../Samples/3rd_String_G_64kb.mp3")
##        data = np.fromstring(sound.raw_data, dtype=np.int16)
##        sr = sound.frame_rate
##        ss = sound.sample_width
##        channels = sound.channels

        # FFT
        freqs, fftData = self.FFT(self.data)

        # find max
        mx = freqs[np.argmax(fftData)]
        
        print("Maximum at: %f Hz" % (mx))

        nearest, f_nearest = getNearest(mx) 
        # freq to cents
        #c = 1200 * math.log2(f_max / f_ref)
        c = 1200 * math.log2(mx / f_nearest)
        print ("offset from closest: %f cents (note: %s)" % (c, nearest))

        #sg.tuning = ["E2", "A2", "D3", "G3", "B3", "E4"] # standard tuning
        #sg.string = 4 #1-6, 1 being lowest pitch 
        ind = sg.tuning[sg.string]
        f_tuning = getFrequency(ind)
        a = 1200 * math.log2(mx / f_tuning)
        # +ve offset -> too sharp, -ve -> too flat

        #setup LEDs using GPIOs 2, 3 and 4
        GPIO.setup(2,GPIO.OUT)
        GPIO.setup(3,GPIO.OUT)
        GPIO.setup(4,GPIO.OUT)

        #make sure they're off when we start (avoids confusion)
        GPIO.output(2,GPIO.LOW)
        GPIO.output(3,GPIO.LOW)
        GPIO.output(4,GPIO.LOW)

        #check if the value for offset, in cents, is between -2 and 2. If so, set Green LED (correctly tuned) to be on and turn others off
        if math.abs(a) < 2:
            GPIO.output(3,GPIO.HIGH)
            GPIO.output(2,GPIO.LOW)
            GPIO.output(4,GPIO.LOW)

        #check if the value for offset, in cents, is greater than/ equal to 2. If so, set right Red LED (too sharp) to be on and turn others off
        elif math.abs(a) >= 2:
            GPIO.output(2,GPIO.HIGH)
            GPIO.output(3,GPIO.LOW)
            GPIO.output(4,GPIO.LOW)

        #check if the value for offset, in cents, is less than/ equal to -2. If so, set left Red LED (too flat) to be on and turn others off
        elif math.abs(a) =< -2:
            GPIO.output(4,GPIO.HIGH)
            GPIO.output(2,GPIO.LOW)
            GPIO.output(3,GPIO.LOW)

            
        print ("Detected note: %s | Target note: %s | Offset (cents): %f" % (nearest, ind, a) )

