#!/usr/bin/env python
# encoding: utf-8
from pyo import *

s = Server(sr=44100, nchnls=2, buffersize=512, duplex=1).boot()


"""Narrow pulses with lots of ripple and some noise give a harsh, gritty, snarling excitation,
    whereas wide pulses with little or no ripple and noise give a smooth, humming source. """
#vocalCords
freq = 100
ripple = 2
width = 40
noisiness = 0.2
        
phasor = Phasor(freq=freq, add=-0.5) #phasor de base

carrier = (Cos(phasor) + 1) * 0.5 #carrier oscille entre 0 et 1, agit comme une enveloppe d'amplitude
modul = Cos(phasor * ripple)

pulses = 1 / (Pow((carrier * modul) * width, 2) + 1) #signal de base des cordes vocales
modNoise = (Noise() * pulses) * noisiness 

pulses = pulses * (1 - noisiness)

cordsOut = Biquad(pulses + modNoise, freq=1, q=1, type=1)

""""""

#vocalTract
base = 90
sep = 120
reso = 45
bankSize = 8
input = cordsOut

freqs = [((i * sep * 1.414) + base) for i in range (bankSize)]

filters = [Biquad(input=input, freq=freqs[i], q=reso, type=2, mul=40) for i in range (bankSize)]


    
s.gui(locals())
