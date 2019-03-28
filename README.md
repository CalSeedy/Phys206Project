# **Dependencies**
- scipy (.signal, numpy and matplotlib)
- pydub (for now)

# **TODO**
- [x] ~~add 'listening' functionality~~ 
- [x] ~~connect to Raspberry Pi~~
- [x] ~~transform data (Fourier)~~
- [x] ~~plot data (original / transformed)~~
- [x] ~~analyse data (find fundamental)~~
- [x] ~~add 6-string functionality for standard tuning~~
- [x] ~~connect LCD to Pi~~
- [x] ~~display text/ arbitrary string to LCD (16 chars max)~~
- [ ] add menu code
- [ ] add up, down, select and switch string buttons
- [ ] link buttons to menu code
- [ ] link all code
- [ ] refactor code and centralise

# **Breakdown**

|:Interface:|:Analysis:|:Debugging/ Visuals:|
|:----------------------------------------------------------------------------------------------------------------------------------------:	|:-----------------------------------------------------------------------------------------------------------------------:	|:----------------------------------------------------------------------------------------------------:	|
| Microphone detection and temp. sound stream storage 	| Take sound as input 	| Format sound data into arrays that correspond to the x and y axis. (time and amplitude respectively) 	|
| Determine when to start or stop recording 	| Use Fast Fourier Transform to transform data from t-space to frequency-space 	| Plot the above formatted  data 	|
| Menu options and what they impact. (Which string we're on/ which tuning mode we are using) 	| Isolate fundamental frequency (and harmonic freqs.?) 	| Plot FFT'd data, with frequency on the x axis and amplitude on y 	|
| UI elements (how the user chooses  the tuning option/ which string they are currently on/ visually show how sharp or flat the string is) 	| Compare against current tuning set, making sure the correct string is selected 	| Update the plotted data every cycle to show "real-time" recording (will help identify any mistakes) 	|
| What happens to the circuit / program when a button is pressed or if the note is too flat or sharp 	| Give a value for how sharp or  flat the string is (maybe from -1 to 1? -1 being too flat, b, and 1 being too sharp, #.) 	|  	|
