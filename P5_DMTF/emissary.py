import suaBibSignal as sbs
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import soundfile   as sf

print("Let the sound begin!")

mySignal = sbs.signalMeu()

signals = mySignal.daTunes()
nSelected = None

symbols = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","#","X"]

print(symbols)
while True:
    nSelected = input("Choose a number from the list above: ")

    if nSelected not in symbols:
        print("Number not available, try again")
    
    else:
        print(f"Wise choice, enjoy the !BASS of the symbol {nSelected}!")
        sd.play(signals[nSelected]["full"])
        sd.wait()
        break

mySignal.plotSig(signals["break"],signals[nSelected]["full"])