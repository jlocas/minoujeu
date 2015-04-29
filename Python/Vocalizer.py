#!/usr/bin/env python
# encoding: utf-8
from pyo import *
import math

"""
REPLIMENT
ENVELOPPES
N'ARRIVE PAS A REMPLACER LES POINTS DES TABLE QUAND ON LOAD UN PRESET

Convertir length de hz en cm?
Sauver les enveloppes dans les presets
Ajouter déviations aléatoires
"""

class Vocalizer:
    def __init__(self, freq=100.0, ripple=1.0, width=1.0, noisiness=0.0, base=100.0, length=10.0, reson=10.0, size=8, freqMod=3.0, baseMod=1.0, lengthMod=1.0, resMod=1.0, dur=1.0):
        self.freq = SigTo(freq, time=0.01, init=freq)
        self.ripple = SigTo(ripple, time=0.01, init=ripple)
        self.width = SigTo(width, time=0.01, init=width)
        self.noisiness = SigTo(noisiness, time=0.01, init=noisiness)
        self.base = SigTo(base, time=0.01, init=base)
        self.length = SigTo(length, time=0.01, init=length)
        self.reson = SigTo(reson, time=0.01, init=reson)
        
        self.dur=dur
        
        self.envArticulate = CosTable()
        self.envAmp = LinTable([(475,0.0000),(1170,1.0000),(6491,0.9038),(8192,0.0000)])
        self.envReader = TableRead(table=[self.envArticulate, self.envAmp], freq=1/self.dur)
        
        self.freqMod = SigTo(self.envReader[0], time=0.05, mul=freqMod)
        self.baseMod = SigTo(self.envReader[0], time=0.05, mul=baseMod)
        self.lengthMod = SigTo(self.envReader[0], time=0.05, mul=lengthMod)
        self.resMod = SigTo(self.envReader[0], time=0.05, mul=resMod)   
        self.outMul = SigTo(self.envReader[1])
        
        self.params = [self.freq, self.ripple, self.width, self.noisiness, self.base, self.length, self.reson,
                                self.freqMod, self.baseMod, self.lengthMod, self.resMod, self.dur]


        #Vocal cords
        self.phasor = Phasor(freq=self.freq * self.freqMod, add=-math.pi, mul=2*math.pi) #phasor de base
        self.modul = (Cos(self.phasor) + 1) * 0.5 #modulateur d'amplitude oscille entre 0 et 1
        self.carrier = Cos(self.phasor * self.ripple)
        self.pulses = 1 / (Pow((self.modul * self.carrier) * self.width, 2) + 1) #signal de base des cordes vocales
        self.modNoise = (Noise() * self.pulses) * self.noisiness 
        self.pulses = self.pulses * (1 - self.noisiness)
        self.cordsOut = Biquad(self.pulses + self.modNoise, freq=1, q=1, type=1) #high pass
        
        #Vocal tract
        self.freqs = [((i * self.length * self.lengthMod * 1.414) + self.base * self.baseMod) for i in range (size)]
        self.filters = [Biquad(input=self.cordsOut, freq=self.freqs[i], q=self.reson * self.resMod, type=2, mul=5) for i in range (size)]
        self.output = Compress((sum(self.filters) / size) * self.outMul, thresh=-30, ratio=3, risetime=0.01, falltime=0.10, lookahead=5.00, knee=0, outputAmp=False, mul=2, add=0)
        

        
    def out(self):
        self.output.out()
        return self
        
    def play(self):
        self.envReader.play()
        
    def setFreq(self, x):
        self.freq.value=x
        
    def setRipple(self, x):
        self.ripple.value=x
        
    def setWidth(self, x):
        self.width.value=x
        
    def setNoisiness(self, x):
        self.noisiness.value=x
        
    def setBase(self, x):
        self.base.value=x
        
    def setLength(self, x):
        self.length.value=x
        
    def setReson(self, x):
        self.reson.value=x
        
    def setDur(self, x):
        self.dur = self.envReader.freq=1/x
        
    def setFreqMod(self, x):
        self.freqMod.mul=x
        
    def setLengthMod(self, x):
        self.lengthMod.mul=x
        
    def setBaseMod(self, x):
        self.baseMod.mul=x
        
    def setResMod(self, x):
        self.resMod.mul=x
        
    def setArticulation(self, lst):
        self.envArticulate.replace(lst)
        
    def setValuesFromPreset(self, lst):
        for i in range(len(lst[0])):
            self.params[i] = lst[0][i]
            
        self.setFreq(self.params[0])
        self.setRipple(self.params[1])
        self.setWidth(self.params[2])
        self.setNoisiness(self.params[3])
        self.setBase(self.params[4])
        self.setLength(self.params[5])
        self.setReson(self.params[6])
        
        self.setFreqMod(self.params[7])
        self.setBaseMod(self.params[8])
        self.setLengthMod(self.params[9])
        self.setResMod(self.params[10])
        self.setDur(self.params[11])
            
        self.setArticulation(lst[1])

    def showArticulation(self):
        self.envArticulate.graph(wxnoserver=True)
        
    def showAmplitude(self):
        self.envAmp.graph(wxnoserver=True)
