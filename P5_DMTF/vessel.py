import suaBibSignal as sbs
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import soundfile   as sf
import time
import peakutils

mySignal = sbs.signalMeu()
fs = 48000
sd.default.samplerate = fs
sd.default.channels = 2
duration = 3


for e in range(3):
    print(f"Starting in {3-e}...")
    time.sleep(1)

print("SENTÔ KAISHI!!!")

nSamples = duration*fs
myRec = sd.rec(int(nSamples), fs, channels=1, blocking=True, dtype="float64")
sd.wait()
print("Time's UP!")
teste = 0
# for e in myRec:
#     if e[0] != e[1]:
#         teste += 1
# print(teste)

# mySignal.plotFFT(myRec, fs)
recFixed = []
for i in range(len(myRec)):
    recFixed.append(myRec[i][0])
sigX, sigY = mySignal.calcFFT(recFixed, fs)

aquiredFs = []
index = peakutils.indexes(np.abs(sigY), thres=0.6, min_dist=50)
print("Peaks indexes {}" .format(index))
for freq in sigX[index]:
    print("Peak frequency is: {}" .format(freq))
    aquiredFs.append(freq)

for key, value in mySignal.nums.items():
    if aquiredFs[0] - 5 <= value[0] and value[0] <= aquiredFs[0] + 5:
        if aquiredFs[1] - 5 <= value[1] and value[1] <= aquiredFs[1] + 5:
            print(f"Somebody pressed the symbol {key}")

plt.plot(recFixed)
plt.grid()
plt.title('Signal on time ;)')
mySignal.plotFFT(recFixed, fs)