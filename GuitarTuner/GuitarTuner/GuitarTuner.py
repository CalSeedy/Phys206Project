#import matplotlib.pyplot as plt
#import numpy as np
import time, matplotlib, pyaudio, sys
from pynput.keyboard import Key, Listener
from referenceFreqs import *

CHUNK = 1024
CHANNELS = 1
SAMPLERATE = 44100
TIME = 5


def preInit():
    global initialised, listening
    listening = False
    initialised = False
    genFreqs()

def initialise():
	global audio, stream, listening, initialised
	audio = pyaudio.PyAudio()
	listening = True
	# Start sound recording
	if (audio.get_device_count() != 0):
		try:
			stream = audio.open(format = pyaudio.paInt16, channels = CHANNELS, rate = SAMPLERATE, input = True, frames_per_buffer = CHUNK)
			initialised = True
			print("Collecting data...")
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
		if not listening:
			close()
			print("Stopping data collection...")
		else:
			listen()
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
    global audio, stream, frames, initialised
    initialised = False
    stream.stop_stream()
    stream.close()
    audio.terminate()

def listen():
    global initialised, listening
    if not initialised:
        initialise()
    while listening:
        with Listener(on_press=on_press) as listener:
            listener.join()
    print(getFreqs('standard'))
    getData()
    update()

preInit()

# Collect events until released
with Listener(on_press=on_press) as listener:
    listener.join()

close()    