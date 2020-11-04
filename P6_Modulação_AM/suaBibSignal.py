
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftshift
from scipy import signal as window

class signalMeu:
    def __init__(self):
        self.init = 0
        self.freqAmostragem = 44100
        self.A = 1.5
        self.T = 2
        self.freqs = [697, 770, 852, 941, 1209, 1336, 1477, 1633]
        self.nums = {
            "1" : [self.freqs[0], self.freqs[4]], 
            "2" : [self.freqs[0], self.freqs[5]], 
            "3" : [self.freqs[0], self.freqs[6]],
            "A" : [self.freqs[0], self.freqs[7]],
            "4" : [self.freqs[1], self.freqs[4]], 
            "5" : [self.freqs[1], self.freqs[5]], 
            "6" : [self.freqs[1], self.freqs[6]], 
            "B" : [self.freqs[1], self.freqs[7]],
            "7" : [self.freqs[2], self.freqs[4]], 
            "8" : [self.freqs[2], self.freqs[5]], 
            "9" : [self.freqs[2], self.freqs[6]],
            "C" : [self.freqs[2], self.freqs[7]],
            "X" : [self.freqs[3], self.freqs[4]], 
            "0" : [self.freqs[3], self.freqs[5]],
            "#" : [self.freqs[3], self.freqs[6]],
            "D" : [self.freqs[3], self.freqs[7]]
            }

    def generateSin(self, freq, amplitude, time, fs):
        n = time*fs
        x = np.linspace(0.0, time, n)
        s = amplitude*np.sin(freq*x*2*np.pi)
        return (x, s)

    def calcFFT(self, signal, fs):
        # https://docs.scipy.org/doc/scipy/reference/tutorial/fftpack.html
        N  = len(signal)
        # W = window.hamming(N)
        T  = 1/fs
        xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
        yf = fft(signal)
        return(xf, np.abs(yf[0:N//2]))

    def plotFFT(self, signal, fs):
        x,y = self.calcFFT(signal, fs)
        plt.figure()
        plt.plot(x, np.abs(y))
        plt.xlim(0, 5000)
        plt.title('Fourier')

    def plotSig(self, breakzin, signal):
        plt.figure()
        plt.plot(breakzin, signal)
        plt.xlim(0, self.T/60)
        plt.title("Signal")
        
    def norm(self, signal):
        high = max(abs(signal)) #Acha o valor máximo para normalizar entre -1 e 1
        return signal/high
    
    def LPF(self, signal, cutoff_hz, fs):
        from scipy import signal as sg
        #####################
        # Filtro
        #####################
        # https://scipy.github.io/old-wiki/pages/Cookbook/FIRFilter.html
        nyq_rate = fs/2
        width = 5.0/nyq_rate
        ripple_db = 60.0 #dB
        N , beta = sg.kaiserord(ripple_db, width)
        taps = sg.firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))
        return( sg.lfilter(taps, 1.0, signal))

    def modSig(self, sig, fs):
        xPort, sinPort = self.generateSin(14000, self.A, len(sig)//fs, fs) 
        return sig*sinPort

    def daTunes(self):
        dic = {}
        fs = self.freqAmostragem
        A = self.A
        T = self.T

        freqDic = {}

        for freq in self.freqs:
            intervalo, freqDic[freq] = self.generateSin(freq, A, T, fs)
            dic["break"] = intervalo

        for key, value in self.nums.items():
            dic[key] = {
                "full" : freqDic[value[0]] + freqDic[value[1]],
                "f1" : freqDic[value[0]],
                "f2" : freqDic[value[1]],
            }

        return dic

# mySignal = signalMeu()
# signales = mySignal.daTunes()
# print(len(signales["break"]))
# mySignal.plotFFT(signales["1"]["f1"], mySignal.freqAmostragem)
# sd.play(signales["5"]["f1"])
# sd.wait()
