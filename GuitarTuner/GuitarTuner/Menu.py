#import necessary modules and files
from threading import Thread
import RPi.GPIO as GPIO
import sharedGlobals as sg
import time, csv

#create a menu class that will control the output to the LCD screen and what options are currently available
class Menu():
    #initialise empty/default values for cycle patterns and states
    upPattern = []
    downPattern = []
    state = 0
    initialised = False
    
    #init function sets the initial values for the menu
    def init(self):
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
