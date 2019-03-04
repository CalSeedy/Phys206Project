#import matplotlib.pyplot as plt
#import numpy as np
import time, matplotlib, pyaudio, sys
from pynput.keyboard import Key, Listener

CHUNK = 1024
CHANNELS = 1
SAMPLERATE = 44100
TIME = 5


listening = False 
initialised = False

def initialise():
    global audio, stream, listening
    audio = pyaudio.PyAudio()
    listening = True
    # Start sound recording
    if (audio.get_device_count() != 0):
        try: 
            stream = audio.open(format = pyaudio.paInt16, channels = CHANNELS, rate = SAMPLERATE, input = True, frames_per_buffer = CHUNK)
        except OSError:
            print("No Microphone Detected...\nTry replugging it in and restarting this program!")
            sys.exit(-9996)
    else:
        print("No Microphone Detected...\nTry replugging it in and restarting this program!")
        sys.exit(-9996)

def on_press(key):
    global listening, initialised

    if key == Key.space:
        listening = not listening
        if not initialised:
            initialise()
            initialised = True
        print("Listening: ", listening)
        

    if key == Key.esc:
        listening = False
        close()    
        sys.exit(0)
        # Stop listener
        return False

def getData():
    global audio, stream, frames

    frames = []
    for i in range(0, int(SAMPLERATE * TIME / CHUNK)):
        data = stream.read(CHUNK)
        frames.append(data)

def update():
    print("")

def close():
    global audio, stream, frames
    initialised = False
    stream.stop_stream()
    stream.close()
    audio.terminate()


# Collect events until released
with Listener(on_press=on_press) as listener:
    listener.join()

if not initialised:
    initialise()

while listening:
    getData()
    update()

close()    
sys.exit(0)