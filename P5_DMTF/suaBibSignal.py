
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
        plt.title('Fourier')

    def plotSig(self, breakzin, signal):
        plt.figure()
        plt.plot(breakzin, signal)
        plt.xlim(0, self.T/60)
        plt.title("Signal")
        

    def daTunes(self):
        dic = {}
        fs = self.freqAmostragem
        A = self.A
        T = self.T
        freqs = [697, 770, 852, 941, 1209, 1336, 1477, 1633]

        freqDic = {}

        for freq in freqs:
            intervalo, freqDic[freq] = self.generateSin(freq, A, T, fs)
            dic["break"] = intervalo
        
        nums = {
            "1" : [freqs[0], freqs[4]], 
            "2" : [freqs[0], freqs[5]], 
            "3" : [freqs[0], freqs[6]],
            "A" : [freqs[0], freqs[7]],
            "4" : [freqs[1], freqs[4]], 
            "5" : [freqs[1], freqs[5]], 
            "6" : [freqs[1], freqs[6]], 
            "B" : [freqs[1], freqs[7]],
            "7" : [freqs[2], freqs[4]], 
            "8" : [freqs[2], freqs[5]], 
            "9" : [freqs[2], freqs[6]],
            "C" : [freqs[2], freqs[7]],
            "X" : [freqs[3], freqs[4]], 
            "0" : [freqs[3], freqs[5]],
            "#" : [freqs[3], freqs[6]],
            "D" : [freqs[3], freqs[7]]
            }

        for key, value in nums.items():
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
