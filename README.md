# **Dependencies**
- matplotlib
- numpy
- pyaudio
- pynput

# **TODO**
- [x] ~~add 'listening' functionality~~ 
- [ ] connect to Raspberry Pi 
- [ ] transform data (Fourier)
- [ ] plot data (original / transformed)
- [ ] analyse data (find fundamental)
- [ ] add 6-string functionality for standard tuning
- [ ] we'll see when we're here...


# **Breakdown**

| Interface 	| Analysis 	| Debugging/ Visuals 	|
|:----------------------------------------------------------------------------------------------------------------------------------------:	|:-----------------------------------------------------------------------------------------------------------------------:	|:----------------------------------------------------------------------------------------------------:	|
| Microphone detection and temp. sound stream storage 	| Take sound as input 	| Format sound data into arrays that correspond to the x and y axis. (time and amplitude respectively) 	|
| Determine when to start or stop recording 	| Use Fast Fourier Transform to transform data from t-space to frequency-space 	| Plot the above formatted  data 	|
| Menu options and what they impact. (Which string we're on/ which tuning mode we are using) 	| Isolate fundamental frequency (and harmonic freqs.?) 	| Plot FFT'd data, with frequency on the x axis and amplitude on y 	|
| UI elements (how the user chooses  the tuning option/ which string they are currently on/ visually show how sharp or flat the string is) 	| Compare against current tuning set, making sure the correct string is selected 	| Update the plotted data every cycle to show "real-time" recording (will help identify any mistakes) 	|
| What happens to the circuit / program when a button is pressed or if the note is too flat or sharp 	| Give a value for how sharp or  flat the string is (maybe from -1 to 1? -1 being too flat, b, and 1 being too sharp, #.) 	|  	|
