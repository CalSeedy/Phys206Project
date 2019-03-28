from threading import Thread
import sharedGlobals as sg
import sys, soundAnalysis#, FFT, Menu, analysis, Input

global Exit

menu = Menu() #screen display
inp = Input() #button inputs
sound = soundAnalysis.Sound() #take sound input and analyse


menuThread = Thread(target=menu.run)
inputThread = Thread(target=inp.run)
soundThread = Thread(target=sound.run)

menuThread.start()
inputThread.start()
soundThread.start()

Exit = False
while not Exit:
    try:
        inp.read()
        menu.display(sg.state)
        sound.run(sg.data)
    except KeyboardInterrupt:
        Exit = True
        
menu.close()
inp.close()
sound.close()

os.exit(0)

