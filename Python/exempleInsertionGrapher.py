#!/usr/bin/env python
# encoding: utf-8
"""
Example d'integration du grapheur de pyo dans une interface maison.

La signature de l'objet Grapher est:
    
class Grapher(wx.Panel):
    def __init__(self, parent, xlen=8192, yrange=(0.0, 1.0), 
                 init=[(0.0,0.0),(1.0,1.0)], mode=0, exp=10.0, 
                 inverse=True, tension=0.0, bias=0.0, outFunction=None)

parent: Le wx.Frame ou wx.Panel dans lequel le graph est place
xlen: Le nombre de points dans la table
yrange: Un tuple indiquant les valeurs minimales et maximales de la table
init: Les points initiaux convertits entre 0 et 1
mode: Le type de table {0: LinTable, 1: CosTable, 2: ExpTable, 3: CurveTable}
exp: Facteur exponentiel (ExpTable)
inverse: Facteur d'inversion (ExpTable)
tension: Facteur de tension (CurveTable) 
bias: Facteur de bias (CurveTable)
outFunction: Fonction automatiquement appelee par le graph avec les nouveaux
             points en argument.

"""

import wx
from pyo import *
# l'objet Grapher doit etre importe de facon explicite
from pyolib._wxwidgets import Grapher

s = Server().boot()

class MyFrame(wx.Frame):
    def __init__(self, parent, title, pos, size):
        wx.Frame.__init__(self, parent, -1, title, pos, size)
        self.panel = wx.Panel(self)

        # la table en question
        self.table = LinTable([(0, 500), (8192, 1000)])
        # lecture en boucle
        self.freqRead = Osc(self.table, freq=1)
        # oscillateur qui recoit les frequences
        self.sine = LFO(freq=self.freqRead, mul=0.1).mix(2).out()

        # gestion du serveur
        onOff = wx.ToggleButton(self.panel, id=-1, label="on / off", 
                                     pos=(10,28), size=wx.DefaultSize)
        onOff.Bind(wx.EVT_TOGGLEBUTTON, self.handleAudio)

        ### preparation du grapheur ###
        # nombre de points dans la table
        xlen = self.table.getSize()
        # liste des points initiaux de la table
        pts = self.table.getPoints()
        # ambitus du grapheur en Y
        yrange = (250, 5000)
        # conversion des points initiaux en valeurs entre 0 et 1
        for i in range(len(pts)):
            x = pts[i][0] / float(xlen)
            y = (pts[i][1] - float(yrange[0])) / (yrange[1]-yrange[0])
            pts[i] = (x,y)

        # le grapheur (mode=0 correspond a un objet LinTable)
        self.graph = Grapher(self.panel, xlen=xlen, yrange=yrange, init=pts, 
                             mode=0, outFunction=self.table.replace)
                             
        self.graph.SetSize((400, 200))
        self.graph.SetPosition((0,0))

        # une boite dans laquelle on affiche les deux objets graphiques
        """box = wx.BoxSizer(wx.VERTICAL)
        box.Add(onOff, 0, wx.ALIGN_CENTER)
        box.Add(self.graph, 1, wx.EXPAND)
        self.panel.SetSizerAndFit(box)"""

        self.Show()

    def handleAudio(self, evt):
        if evt.GetInt() == 1:
            s.start()
        else:
            s.stop()

app = wx.App(False)
mainFrame = MyFrame(None, title='Test Insert Graph', 
                    pos=(100,100), size=(500,300))
app.MainLoop()
