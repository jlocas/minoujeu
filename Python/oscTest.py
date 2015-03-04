#!/usr/bin/env python
# encoding: utf-8
from pyo import *

s = Server(sr=44100, nchnls=2, buffersize=512, duplex=1).boot()



def OSC(address, *args):
    if address == '/mj/mouse/squeak':
        if args == (1,): 
            print "squeaksqueak"
        
    print args
    #print address

a = OscDataReceive(44444, "/mj/*", OSC)



s.gui(locals())
