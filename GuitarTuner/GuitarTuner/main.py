from threading import Thread, Lock
import sharedGlobals as sg
import sys, soundAnalysis, Input

threads = []

#create input and analysis instances
inp = Input.Input()
sound = soundAnalysis.Sound()

# create thread with those instances and target their run function
inpThread = Thread(target=inp.run)
soundThread = Thread(target=sound.run)

# add the threads to the thread list 
threads.append(inpThread)
threads.append(soundThread)

# start the threads
inpThread.start()
soundThread.start()

# wait until both threads are finished
for i in threads:
    i.join()

print("Finished")

