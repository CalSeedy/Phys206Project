import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import fft,fftfreq, ifft

#number of points
n = 1000
#time in second
t = 100
#angular frequency
w = 2.0*np.pi/t
#individual signals
x  = np.linspace(0, t, n)
y1 = 1.0*np.cos(5.0*w*x)
y2 = 2.0*np.sin(10.0*w*x)
y3 = 0.5*np.sin(20.0*w*x)
#superposition signal
y = y1 + y2 + y3
#cretaes all necessary frequencies
freqs = fftfreq(n)
#need mask array to get rid of half the values as they are the complex conjugate
mask = freqs > 0
#fft values
fft_vals = fft(y)
#true theoretical fft
fft_theo = 2.0*np.abs(fft_vals/n)
#original signal
plt.figure(1)
plt.title('Original Signal')
plt.plot(x, y, color='xkcd:blue', label='original')
plt.legend()

#FFT Plot
plt.figure(2)
#plt.plot(freqs,fft_vals,color='blue',label='Raw FFT')
#plt.title('FFT')
plt.plot(freqs[mask],fft_theo[mask],label='FFT Values')
plt.title('FFT Values')
plt.draw()


