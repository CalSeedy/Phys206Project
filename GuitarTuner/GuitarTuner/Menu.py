from threading import Thread
import RPi.GPIO as GPIO
import sharedGlobals as sg
import time, csv

class Menu():
    options = []
    upPattern = []
    downPattern = []
    state = 0
    
    def __init__(self):
        
        #load options
        print("Sound thread: starting ")
        self.options = ["Guitar Tuner", "Press Select..."]
        self.state = 0

    def cycle(self, direction):
        pattern = []
        if len(self.upPattern) == 0 or len(self.downPattern) == 0:
            raise Exception("Pattern(s) not set...")
        else:
            if (direction == 0):
                pattern = self.upPattern
            elif (direction == 1):
                pattern = self.downPattern
            else:
                raise Exception("Expected 0 or 1, received %s" % (str(direction)))
            
        self.options = [self.options[i] for i in pattern]

    def loadCustoms():
        try:
            with open("customs.csv", "r") as readFile:
                reader = csv.reader(readFile)
                i = 1
                options = []
                for row in readFile:
                    row = row.split(",")
                    #print("Loading option: %s ...(%d/%d)" % (row[0], i, count))
                    options.append(row[1], row[2], row[3], row[4], row[5], row[6])
                    i += 1
                readFile.close()
            self.options = options + ["Exit..."]
            if len(self.options):
                self.downPattern = [(x+1) for x in range(len(self.options)-1)] + [0]
                self.upPattern = [len(self.options) - 1] + [x for x in range(len(self.options)-1)]
        
        except Exception:
            raise("custom mode file doesn't exit...\nCreate new 'customs.csv' file")


    def loadPresets():
        
        with open("tunings.csv", "r") as readFile:
            reader = csv.reader(readFile)
            tunings = []            
            for row in readFile:
                row = row.split(",")
                tunings.append(row[0])
            readFile.close()
            
            self.options = tunings + ["Exit..."]
            
            self.downPattern = [(x+1) for x in range(len(self.options)-1)] + [0]
            self.upPattern = [len(self.options) - 1] + [x for x in range(len(self.options)-1)]
    
        
    def run(self):
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
         
        def main(self):
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
            
            while sg.running:
                print("Menu thread: running ")
                if (self.state == 0):
                    self.options = ["Guitar Tuner", "Press Select..."]
                # Send some test
                if len(options) > 2:
                    lcd_string(options[0], LCD_LINE_1)
                    lcd_string(options[1], LCD_LINE_2)
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
