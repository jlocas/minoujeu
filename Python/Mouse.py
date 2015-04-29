#!/usr/bin/env python
# encoding: utf-8
from pyo import *
from Vocalizer import *
import os, random


"""cette classe doit:
        récupérer un preset dans le folder presets
        assigner les parametres du preset a vocalizer
        jouer
"""
server = Server(sr=96000, nchnls=1).boot()

class Mouser:
    def __init__(self, audio):
        self.path = os.path.join(os.getcwd(), "Presets")
        self.audio = audio
        
        #freq, ripple, width, noise, base, length, reson, fmod, bmod, lmod, rmod, dur
        self.preset1 = [[1892.2, 1.304, 1.00, 0.010, 1218.26, 1367.246, 11.5, 2.81, 1.99, 1.99, 2.47, 0.29], [(0, 1.0), (1206, 0.9807692307692307), (3072, 0.6217948717948718), (5906, 0.5705128205128205), (8191, 1.0)]]
        self.preset2 = [[2180.0, 1.304, 1.00, 0.010, 1528.26, 1367.246, 11.5, 2.28, 1.99, 1.99, 2.47, 0.38], [(0, 1.0), (1499, 0.532051282051282), (3986, 0.4358974358974359), (4224, 0.9038461538461539), (5760, 0.391025641025641), (8191, 1.0)]]
        self.preset3 = [[2380.0, 1.304, 1.00, 0.01, 1937.54, 789.855, 7.9, 3.07, 3.97, 3.77, 1.00, 0.2], [(0, 1.0), (1371, 0.9230769230769231), (5357, 0.6025641025641025), (8191, 1.0)]]
        self.preset4 = [[2880.0, 1.304, 1.00, 0.01, 1937.54, 789.855, 7.9, 3.07, 3.97, 3.77, 2.00, 0.17], [(0, 1.0), (1554, 0.2692307692307692), (2578, 0.8974358974358975), (3657, 0.46153846153846156), (3894, 0.9230769230769231), (4973, 0.782051282051282), (5833, 0.9166666666666666), (7149, 0.6730769230769231), (8191, 1.0)]]
        self.preset5 = [[2680.0, 1.304, 1.00, 0.01, 1937.54, 789.855, 7.9, 2.47, 3.97, 3.82, 1.00, 0.47], [(0, 1.0), (1956, 0.8589743589743589), (2560, 0.3782051282051282), (4370, 1.0), (6217, 0.6346153846153846), (8191, 1.0)]]
        self.presets = [self.preset1, self.preset2, self.preset3, self.preset4, self.preset5]
        
    def buildPreset(self):
        self.vallst = []
        
        self.preset = random.choice(self.presets)
        self.tablst = self.preset[1]
        
        for i in range(len(self.audio.params)):
            self.preset = random.choice(self.presets)
            self.value = self.preset[0][i]
            self.value = self.value + (self.value * random.uniform(-0.1, 0.1))
            self.vallst.append(self.value)
            
        self.lst = [self.vallst, self.tablst]
        self.audio.setValuesFromPreset(self.lst)
        self.audio.play()

            
        
            
    def newPreset(self):
        self.choice = random.choice(self.presets)
        self.audio.setValuesFromPreset(self.choice)
        self.audio.play()

audio = Vocalizer()
audio.out()
mouse = Mouser(audio=audio)



def OSC(address, *args):
    if address == '/mj/mouse/squeak':
        if args == (1,): 
            #print "allo"
            mouse.buildPreset()
        

a = OscDataReceive(44444, "/mj/*", OSC)


        
server.gui(locals())
