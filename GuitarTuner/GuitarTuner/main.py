from multiprocessing import Process
import sharedGlobals as sg
import sys, soundAnalysis, Input

if __name__ == "__main__":
    #create input and analysis instances
    inp = Input.Input()
    sound = soundAnalysis.Sound()

    # create thread with those instances and target their run function
    inpProc = Process(target = inp.run)
    soundProc = Process(target = sound.run)

    # add the threads to the thread list 
    sg.procs.append(inpProc)
    sg.procs.append(soundProc)

    if len(sg.procs) > 0:
        for proc in sg.procs:
            proc.start()
            
print("Finished")

