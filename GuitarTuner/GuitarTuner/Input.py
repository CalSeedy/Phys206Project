import RPi.GPIO as GPIO
import sharedGlobals as sg
from multiprocessing import Process
import time, Menu

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
    def init(self):
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
    



