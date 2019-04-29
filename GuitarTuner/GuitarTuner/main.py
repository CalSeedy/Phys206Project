#import necessary modules and files
from multiprocessing import Process
import sharedGlobals as sg
import sys, soundAnalysis, Input

if __name__ == "__main__":
    #create input and analysis class instances
    inp = Input.Input()
    sound = soundAnalysis.Sound()

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
            
