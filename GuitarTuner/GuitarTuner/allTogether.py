#import necessary files and modules
import RPi.GPIO as GPIO
import sharedGlobals as sg
#import pydub as pd
import numpy as np
import scipy.signal as sps
import matplotlib.pyplot as plt
import math, csv, serial, sys
from numpy.fft import fft, fftfreq
from multiprocessing import Process

            
##### SOUND STUFF
#create a sound class that controls anything to do with the sound input and output, including intermediate steps (i.e. analysis and transformation)
class Sound():
    #create variables for storing the sound data, USB serial and initialisation state
    data = []
    ser = 0
    initialised = False

    #init function sets the USB serial and sets the initialisation to true
    def __init__(self):
        self.ser = serial.Serial("/dev/ttyACM0", sg.rate)
        self.initialised = True

    #getData checks the serial for any incoming data and builds a buffer of 1024 values before setting the shared data variable to this buffer
    def getData(self):
        data = []
        i = 0
        self.ser.reset_input_buffer()
        while len(data) < 10:
            if self.ser.inWaiting() > 0:
                
                byteData = self.ser.read(sys.getsizeof(int))
                
##                #take byte data, decode it into a string, then get rid of trailing whitespaces
##                string = read.decode().rstrip()
##                i = 0
##                ints = []
##                for char in string:
##                    if char == ".":
##                        break
##                    else:
##                        i += 1
##
##                power = (len(string) - i)
##                integer = []
##                fract = []
##                for x in range(i):
##                    integer.append(string[x])
##                integer = int("".join(integer))
##
##                for x in range(len(string) - i - 1):
##                    fract.append(string[x + i + 1])
##                fract = int("".join(fract))
##                value = float(integer) + float(fract) / (10**(len(string) - i - 1))
                data.append(read)
                
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
            self.getData()
            
            #transform data
            fftData = self.FFT(self.data)

            #analyse data (find peak and compare)
            self.analyse(fftData)
            
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



##### MENU STUFF

class Menu():
    #initialise empty/default values for cycle patterns and states
    upPattern = []
    downPattern = []
    state = 0
    initialised = False
    
    #init function sets the initial values for the menu
    def __init__(self):
        #set common options for initial screen for the tuner
        sg.options = ["Guitar Tuner", "Press Select..."]
        
        #initial state is 0 (starting screen)
        self.state = 0
        
        #acknowledge when initialised
        self.initialised = True

    #cycle function takes a direction, 0 = up / 1 = down and cycles the options either 1 up or 1 down
    def cycle(self, direction):
        #create a local storage for the cycle pattern
        pattern = []
        
        #make sure that the patterns for each direction have been defined
        if len(self.upPattern) == 0 or len(self.downPattern) == 0:
            #if not, raise an error, we can't continue
            raise Exception("Pattern(s) not set...")
        else:
            #if so, and the direction is up... cycle the options with the up pattern
            if (direction == 0):
                pattern = self.upPattern
                
            #if so, and the direction is down... cycle the options with the down pattern
            elif (direction == 1):
                pattern = self.downPattern
            #if so, and the direction isn't 1 or 0... raise an error, we can't continue with that
            else:
                raise Exception("Expected 0 or 1, received %s" % (str(direction)))
        
        #store the new local options in the shared options variable
        sg.options = [sg.options[i] for i in pattern]
    
    #loadCustoms function takes all user created tuning sets and loads them into the options variable
    def loadCustoms():
        #try to load the custom tunings csv
        try:
            with open("customs.csv", "r") as readFile:
                reader = csv.reader(readFile)
                options = []
                #look at every row and split the string into the tuning name and the notes
                for row in readFile:
                    row = row.split(",")
                    #append (add) tuning name to list of options
                    options.append(row[0])
                    
                readFile.close()
            #set shared options variable to the list we created, with an "Exit" added on the end
            sg.options = options + ["Exit..."]
            
            #generate the up and down cycle patterns for the loaded list of options
            if len(sg.options):
                self.downPattern = [(x+1) for x in range(len(sg.options)-1)] + [0]
                self.upPattern = [len(sg.options) - 1] + [x for x in range(len(sg.options)-1)]
                
        #if there is no custom tunings file, we cant continue
        except Exception:
            raise("custom mode file doesn't exit...\nCreate new 'customs.csv' file")

    #loadPresets function loads the preset tuning modes and adds them to the shared options variable
    def loadPresets():
                
        #load the preset tunings csv
        with open("tunings.csv", "r") as readFile:
            reader = csv.reader(readFile)
            tunings = []
            #for every row, append the name of the tuning
            for row in readFile:
                row = row.split(",")
                tunings.append(row[0])
            readFile.close()
            
            #set the shared options to the tuning list + an "Exit" option
            sg.options = tunings + ["Exit..."]
            
            #generate the up and down patterns from preset options
            self.downPattern = [(x+1) for x in range(len(sg.options)-1)] + [0]
            self.upPattern = [len(sg.options) - 1] + [x for x in range(len(sg.options)-1)]
    
    #run function runs constantly while the menu is needed to be displayed
    def run(self):
        #if the menu isn't initialised, initialise it and continue
        if not self.initialised:
            self.init()
            
        # Define GPIO to LCD mapping
        LCD_RS = 7
        LCD_E  = 8
        LCD_D4 = 25
        LCD_D5 = 24
        LCD_D6 = 23
        LCD_D7 = 18
         
        # Define some device constants
        LCD_WIDTH = 16    # Maximum characters per line
        LCD_CHR = True
        LCD_CMD = False
         
        LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
        LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
         
        # Timing constants
        E_PULSE = 0.0005
        E_DELAY = 0.0005
         
        def main():
            # Main program block
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
            GPIO.setup(LCD_E,  GPIO.OUT) # E
            GPIO.setup(LCD_RS, GPIO.OUT) # RS
            GPIO.setup(LCD_D4, GPIO.OUT) # DB4
            GPIO.setup(LCD_D5, GPIO.OUT) # DB5
            GPIO.setup(LCD_D6, GPIO.OUT) # DB6
            GPIO.setup(LCD_D7, GPIO.OUT) # DB7
            
            # Initialise display
            lcd_init()
            
            #while we want to be displaying data
            while sg.running:
                
                #if we are on the initial screen
                if (self.state == 0):
                    #set the shared options variable to the starting list
                    sg.options = ["Guitar Tuner", "Press Select..."]
                    
                #if there are options to display, show the 1st two on separate lines
                if len(sg.options) > 0:
                    lcd_string(sg.options[0], LCD_LINE_1)
                    lcd_string(sg.options[1], LCD_LINE_2)
                else:
                    lcd_string("Error", LCD_LINE_1)
                    lcd_string("len(options) = 0", LCD_LINE_2)
                time.sleep(0.1)
            lcd_byte(0x01, LCD_CMD)
            lcd_string("Goodbye!",LCD_LINE_1)
            GPIO.cleanup()
            
            
            
        def lcd_init():
            # Initialise display
            lcd_byte(0x33,LCD_CMD) # 110011 Initialise
            lcd_byte(0x32,LCD_CMD) # 110010 Initialise
            lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
            lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
            lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
            lcd_byte(0x01,LCD_CMD) # 000001 Clear display
            time.sleep(E_DELAY)
         
        def lcd_byte(bits, mode):
            # Send byte to data pins
            # bits = data
            # mode = True  for character
            #        False for command
         
            GPIO.output(LCD_RS, mode) # RS
         
            # High bits
            GPIO.output(LCD_D4, False)
            GPIO.output(LCD_D5, False)
            GPIO.output(LCD_D6, False)
            GPIO.output(LCD_D7, False)
            if bits&0x10==0x10:
                GPIO.output(LCD_D4, True)
            if bits&0x20==0x20:
                GPIO.output(LCD_D5, True)
            if bits&0x40==0x40:
                GPIO.output(LCD_D6, True)
            if bits&0x80==0x80:
                GPIO.output(LCD_D7, True)

            # Toggle 'Enable' pin
            lcd_toggle_enable()

            # Low bits
            GPIO.output(LCD_D4, False)
            GPIO.output(LCD_D5, False)
            GPIO.output(LCD_D6, False)
            GPIO.output(LCD_D7, False)
            if bits&0x01==0x01:
                GPIO.output(LCD_D4, True)
            if bits&0x02==0x02:
                GPIO.output(LCD_D5, True)
            if bits&0x04==0x04:
                GPIO.output(LCD_D6, True)
            if bits&0x08==0x08:
                GPIO.output(LCD_D7, True)

            # Toggle 'Enable' pin
            lcd_toggle_enable()

        def lcd_toggle_enable():
            # Toggle enable
            time.sleep(E_DELAY)
            GPIO.output(LCD_E, True)
            time.sleep(E_PULSE)
            GPIO.output(LCD_E, False)
            time.sleep(E_DELAY)

        def lcd_string(message,line):
            # Send string to display

            message = message.ljust(LCD_WIDTH," ")

            lcd_byte(line, LCD_CMD)

            for i in range(LCD_WIDTH):
                lcd_byte(ord(message[i]),LCD_CHR)
        main()


##### INPUT STUFF
#Input class handles everthing to do with button presses and their current state.
class Input():
    #give arbitrary values to each button so we know if they've been correctlt set
    pin_UP = -1
    pin_DWN = -1
    pin_SEL = -1
    pin_NXT = -1

    #same as above
    menu = 0
    menuProc = 0
    initialised = False

    #init function sets all necessary values for button GPIOs and creates the Menu, since the buttons
    #control the state of the menu.
    def __init__(self):
        #print("Input thread: starting ")
        self.menu = Menu.Menu() #create menu
        self.menuProc = Process(target = self.menu.run)
        sg.procs.append(self.menuProc)
        self.menuProc.start()
        GPIO.setmode(GPIO.BCM)
        self.pin_UP = 5
        self.pin_DWN = 6
        self.pin_SEL = 13
        self.pin_NXT = 19

        #if the button values didn't change, something went wrong and we can't continue
        if (self.pin_UP == -1) or (self.pin_DWN == -1) or (self.pin_SEL == -1) or (self.pin_NXT == -1):
            raise Exception("Couldn't match buttons to GPIO pins!")
        
        GPIO.setup(self.pin_UP , GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.pin_DWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.pin_SEL, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.pin_NXT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.initialised = True

    #run funtion is the main code block for the Input class. Here, the state of the buttons are checked at each loop,
    #if a specific button is pressed at some specific point, then the program will proceed accordingly.
    def run(self):
        
        #make sure we have been initialised
        if not self.initialised:
            self.init()
            
        #while we want to be taking button inputs
        while sg.running:
            #print(sg.options)

            #print("Input thread: running ")
            
            #define the button states
            up = GPIO.input(self.pin_UP)
            dwn = GPIO.input(self.pin_DWN)
            sel = GPIO.input(self.pin_SEL)
            nxt = GPIO.input(self.pin_NXT)

            #check if we want to exit before anything else
            if self.menu.state == -1:
                sg.running = False

            #check if up button is pressed and ,if so, cycle the menu upwards
            if (up):
                print("up pressed")
                #change menu
                if (self.menu.state > 0):
                    self.menu.cycle(0)
                    
            #check if down button is pressed and ,if so, cycle the menu downwards
            elif (dwn):
                print("down pressed")
                #change menu
                if (self.menu.state > 0):
                    self.menu.cycle(1)
                    
            #check if select button is pressed and ,if so, do the corresponding action (dependent on the current state)
            elif (sel):
                
                if (self.menu.state > 0) and (self.menu.options[0] == "Exit..."):
                    self.menu.state -= 1
                    
                elif (self.menu.state == 0):
                    self.menu.state += 1
                    
                elif (self.menu.state == 1) and self.menu.options[0] == "Custom Modes":
                    self.menu.state = 5 #custom mode state
                    self.menu.options = self.menu.loadCustoms()
                    
                elif (self.menu.state == 1) and self.menu.options[0] == "Preset Modes":
                    self.menu.state = 2 #preset mode state
                    self.menu.options = self.menu.loadPresets()
                    
            #check if next string button is pressed and ,if so, cycle to the next string  
            elif (nxt):
                #change menu
                if (self.menu.state == 2): 
                    sg.string = (sg.string + 1) % 6
            
            time.sleep(0.3)

if __name__ == "__main__":
    #create input and analysis class instances
    inp = Input()
    sound = Sound()

    # create new subprocess with those instances and target their run function
    inpProc = Process(target = inp.run)
    soundProc = Process(target = sound.run)

    # add the processes to the process list 
    sg.procs.append(inpProc)
    sg.procs.append(soundProc)
    
    # start all the processes in the list
    if len(sg.procs) > 0:
        for proc in sg.procs:
            proc.start()
