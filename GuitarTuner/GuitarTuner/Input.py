import RPi.GPIO as GPIO
import sharedGlobals as sg
from threading import Thread
import time, Menu

class Input():
    pin_UP = -1
    pin_DWN = -1
    pin_SEL = -1
    pin_NXT = -1
    
    menu = 0
    menuThread = 0

    def __init__(self):
        self.menu = Menu.Menu() #create menu menu
        self.menuThread = Thread(target=self.menu.run)
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

    def run(self):
        while sg.running:
            up = GPIO.input(pin_UP)
            dwn = GPIO.input(pin_DWN)
            sel = GPIO.input(pin_SEL)
            nxt = GPIO.input(pin_NXT)
    
            if (up):
                #change menu
                if (self.menu.state > 0):
                    self.menu.cycle(0)
                time.sleep(0.3)
                
            elif (dwn):
                #change menu
                if (self.menu.state > 0):
                    self.menu.cycle(1)
                time.sleep(0.3)
                
            elif (sel):
                
                if (self.menu.state > 0) and (self.menu.option[0] == "Exit..."):
                    self.menu.state -= 1
                    
                elif (self.meun.state == 0):
                    self.menu.state += 1
                    
                elif (self.menu.state == 1) and self.menu.options[0] == "Custom Modes":
                    self.menu.state = 5 #custom mode state
                    options = self.menu.loadCustoms()
                    
                elif (self.menu.state == 1) and self.menu.options[0] == "Preset Modes":
                    self.menu.state = 2 #preset mode state
                    options = self.menu.loadPresets()
                    
                time.sleep(0.3)
                
            elif (nxt):
                #change menu
                if (self.menu.state == 2): 
                    sg.string = (sg.string + 1) % 6
                time.sleep(0.3)
    



