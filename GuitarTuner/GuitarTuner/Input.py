import RPi.GPIO as GPIO
import sharedGlobals as sg
from multiprocessing import Process
import time, Menu

class Input():
    pin_UP = -1
    pin_DWN = -1
    pin_SEL = -1
    pin_NXT = -1
    
    menu = 0
    menuProc = 0
    initialised = False
    
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
        
        if (self.pin_UP == -1) or (self.pin_DWN == -1) or (self.pin_SEL == -1) or (self.pin_NXT == -1):
            raise Exception("Couldn't match buttons to GPIO pins!")
        
        GPIO.setup(self.pin_UP , GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.pin_DWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.pin_SEL, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.pin_NXT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.initialised = True

    def run(self):
        if not self.initialised:
            self.init()
            
        while sg.running:
            print(sg.options)

            #print("Input thread: running ")
            up = GPIO.input(self.pin_UP)
            dwn = GPIO.input(self.pin_DWN)
            sel = GPIO.input(self.pin_SEL)
            nxt = GPIO.input(self.pin_NXT)

            if self.menu.state == -1:
                sg.running = False
            
            if (up):
                print("up pressed")
                #change menu
                if (self.menu.state > 0):
                    self.menu.cycle(0)
                
            elif (dwn):
                print("down pressed")
                #change menu
                if (self.menu.state > 0):
                    self.menu.cycle(1)
                
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
                    
                
            elif (nxt):
                #change menu
                if (self.menu.state == 2): 
                    sg.string = (sg.string + 1) % 6
            
            time.sleep(0.3)
    



