#!/usr/bin/env python
# encoding: utf-8
import wx, os
from Vocalizer import *
from pyo import *
from pyolib._wxwidgets import Grapher

"""
Bug avec les tables:
    Premièrement, les tables ne s'affiche pas sans la ligne wx.CallAfter(self.showWidgets) (ligne 146) qui appelle la méthode graph des tables dans Vocalizer.
    Si on n'appelle pas showWidgets, les tables prennent beaucoup de temps à s'afficher et ça ne fonctionne pas lorsqu'elles le sont. Elles sont mal initialisées
    et ça plante quand on essaie d'ajouter des points. Il me semble que les tables devraient afficher sans showWidgets.
    
    Ensuite, je n'arrive à afficher seulement une table sans problème. Si j'essais d'afficher les 2 en même temps et que je tente de modifier la deuxième,
    ça plante. De plus, la deuxième ne semble pas s'initialiser correctement.
    
    J'ai essayé plusieurs modifications, mais ça revient toujours au même. Les seules différences que je vois par rapport au code d'exemple sont que je
    n'utilise pas de sizer, j'assigne des size et des position et mes tables se trouvent dans une classe différente que le Grapher.
    
    Au fond, on dirait que seulement la table qui a été affichée par graph() puisse être dessinée par le Grapher.
"""


class Audio:
    def __init__(self, pan=0.5):
        self.server = Server(sr=96000, nchnls=1).boot()
        self.vocal = Vocalizer().out()

class MainFrame(wx.Frame):

    def __init__(self, parent, title, pos, size, audio):
        wx.Frame.__init__(self, parent, id=-1, title=title, pos=pos, size=size)
        self.mainPanel = wx.Panel(self)
        self.mainPanel.SetBackgroundColour("#111111")
        self.audio = audio
        
        self.artiTable = self.audio.vocal.envArticulate
        self.ampTable = self.audio.vocal.envAmp
        self.artiTable = CosTable()
        self.ampTable = LinTable()
        
        
        """Boutons"""
        self.serverTog = ToggleButton(self, pos=(0,0), label="Start", handler=self.handleServer)
        self.playButton = Button(self, pos=(100, 0), label="Play!", handler=self.handlePlay)
        
        self.path = os.path.join(os.getcwd(), "Presets")
        pstlist = [f for f in os.listdir(self.path)]
        self.presetChoice = wx.Choice(self, -1, choices=pstlist, pos=(200, 0))
        #self.presetchoiceText = wx.StaticText(self.presetChoice, -1, "Preset", pos=(-10, 0))

        
        """parametres de menu"""
        menubar = wx.MenuBar()
        menu = wx.Menu()
        menu.Append(100, "Save Preset\tCtrl+S")
        menu.Append(101, "Load Preset\tCtrl+L")
        menubar.Append(menu, "File")
        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.OnSave, id=100)
        self.Bind(wx.EVT_MENU, self.OnLoad, id=101)
        
        """parametres generaux"""
        self.fp = 1000 #precision des décimals des valeurs
        self.fpm = 1.0 / self.fp
        self.sliderSep = 90 #espace entre chaque slider
        self.panelSep = 10
        
        self.sliderOffsetX = 10 #offset par rapport au parent
        self.sliderOffsetY = 70
        self.labelOffsetY = -25
        self.valuesOffsetY = 20
        
        self.labelSize = 15
        self.valuesSize = 12
        
        self.cordPanelSize = [250, 450]
        self.tractPanelSize = [250, 450]
        self.dynaPanelSize = [250, 500]
        
        self.panelColor = "#FFFFFF"
        idCount=0

        
        """CORDES VOCALES"""
        self.cordPanel = Panel(parent=self, label="Vocal Cords", pos=(0,50), size=(self.cordPanelSize[0], self.cordPanelSize[1]), color=self.panelColor, font=[15, wx.NORMAL, wx.BOLD])
        self.cordSliders = [0,0,0,0]
        self.cordLabels = [0,0,0,0]
        self.cordValues = [0,0,0,0]
        self.cordParams = [["Frequency (Hz)", 400, 20, 8000, 1, self.handleCordFreq], ["Ripple", 0.2, 0, 5, 3, self.handleRipple], ["Width", 1, 1, 100, 2, self.handleWidth], ["Noisiness", 0, 0, 1, 3, self.handleNoisiness]]
        for i in range(0, 4): #creation des sliders selon le ratio de separation, les parametres et les offsets
            self.cordSliders[i] = Slider(parent=self.cordPanel, value=self.cordParams[i][1] * pow(10, self.cordParams[i][4]), min=self.cordParams[i][2] * pow(10, self.cordParams[i][4]), max=self.cordParams[i][3] * pow(10, self.cordParams[i][4]), pos=(0 + self.sliderOffsetX, self.sliderSep*i + self.sliderOffsetY), size=(self.cordPanelSize[0] - self.sliderOffsetX*2, 20), handler=self.cordParams[i][5])
            #affichage des labels
            self.cordLabels[i] = Label(parent=self.cordPanel, pos=(0 + self.sliderOffsetX, (self.sliderSep*i) + self.sliderOffsetY + self.labelOffsetY), text=self.cordParams[i][0], font=[self.labelSize, wx.NORMAL, wx.NORMAL])
            self.cordLabels[i].CenterOnParent(dir=wx.HORIZONTAL)
            #affichage des valeurs
            self.cordValues[i] = Label(parent=self.cordPanel, pos=(0 + self.sliderOffsetX, (self.sliderSep*i) + self.sliderOffsetY + self.valuesOffsetY), text=("%.2f" % self.cordParams[i][1]), font=[self.valuesSize, wx.NORMAL, wx.NORMAL])
            self.cordValues[i].CenterOnParent(dir=wx.HORIZONTAL)
            idCount += 1
            
        """TRACTUS VOCAL"""
        self.tractPanel = Panel(parent=self, label="Vocal Tract", pos=(self.panelSep + self.cordPanelSize[0], 50), size=(self.tractPanelSize[0], self.tractPanelSize[1]), color=self.panelColor, font=[15, wx.NORMAL, wx.BOLD])
        self.tractSliders = [0,0,0]
        self.tractLabels = [0,0,0]
        self.tractValues = [0,0,0]
        self.tractParams = [["Base", 20, 10, 4000, 2, self.handleTractBase], ["Length", 0.2, 20, 5000, 3, self.handleTractLength], ["Resonance", 10, 5, 60, 1, self.handleTractResonance]] #parametre, val, min, max, precision, handler
        for i in range(0, 3): #creation des sliders selon le ratio de separation, les parametres et les offsets
            self.tractSliders[i] = Slider(parent=self.tractPanel, value=self.tractParams[i][1] * pow(10, self.tractParams[i][4]), min=self.tractParams[i][2] * pow(10, self.tractParams[i][4]), max=self.tractParams[i][3] * pow(10, self.tractParams[i][4]), pos=(0 + self.sliderOffsetX, self.sliderSep*i + self.sliderOffsetY), size=(self.tractPanelSize[0] - self.sliderOffsetX*2, 20), handler=self.tractParams[i][5])
            #affichage des labels
            self.tractLabels[i] = Label(parent=self.tractPanel, pos=(0 + self.sliderOffsetX, (self.sliderSep*i) + self.sliderOffsetY + self.labelOffsetY), text=self.tractParams[i][0], font=[self.labelSize, wx.NORMAL, wx.NORMAL])
            self.tractLabels[i].CenterOnParent(dir=wx.HORIZONTAL)
            #affichage des valeurs
            self.tractValues[i] = Label(parent=self.tractPanel, pos=(0 + self.sliderOffsetX, (self.sliderSep*i) + self.sliderOffsetY + self.valuesOffsetY), text=("%.2f" % self.tractParams[i][1]), font=[self.valuesSize, wx.NORMAL, wx.NORMAL])
            self.tractValues[i].CenterOnParent(dir=wx.HORIZONTAL)
            
        """DYNAMIQUE"""
        self.dynaPanel = Panel(parent=self, label="Dynamics", pos=(self.panelSep*2 + self.tractPanelSize[0] + self.cordPanelSize[0], 50), size=(self.dynaPanelSize[0], self.dynaPanelSize[1]), color=self.panelColor, font=[15, wx.NORMAL, wx.BOLD])
        self.dynaSliders = [0,0,0,0,0]
        self.dynaLabels = [0,0,0,0,0]
        self.dynaValues = [0,0,0,0,0]
        self.dynaParams = [["Frequency Mod", 1, 0.01, 10, 2, self.handleFreqMod], ["Base Mod", 1, 0.01, 10, 2, self.handleBaseMod], ["Length Mod", 1, 0.01, 10, 2, self.handleLengthMod], ["Resonance Mod", 1, 0.01, 10, 2, self.handleResoMod], ["Duration", 1, 0.01, 19, 2, self.handleDur]] #parametre, val, min, max, precision, handler
        for i in range(0, 5): #creation des sliders selon le ratio de separation, les parametres et les offsets
            self.dynaSliders[i] = Slider(parent=self.dynaPanel, value=self.dynaParams[i][1] * pow(10, self.dynaParams[i][4]), min=self.dynaParams[i][2] * pow(10, self.dynaParams[i][4]), max=self.dynaParams[i][3] * pow(10, self.dynaParams[i][4]), pos=(0 + self.sliderOffsetX, self.sliderSep*i + self.sliderOffsetY), size=(self.dynaPanelSize[0] - self.sliderOffsetX*2, 20), handler=self.dynaParams[i][5])
            #affichage des labels
            self.dynaLabels[i] = Label(parent=self.dynaPanel, pos=(0 + self.sliderOffsetX, (self.sliderSep*i) + self.sliderOffsetY + self.labelOffsetY), text=self.dynaParams[i][0], font=[self.labelSize, wx.NORMAL, wx.NORMAL])
            self.dynaLabels[i].CenterOnParent(dir=wx.HORIZONTAL)
            #affichage des valeurs
            self.dynaValues[i] = Label(parent=self.dynaPanel, pos=(0 + self.sliderOffsetX, (self.sliderSep*i) + self.sliderOffsetY + self.valuesOffsetY), text=("%.2f" % self.dynaParams[i][1]), font=[self.valuesSize, wx.NORMAL, wx.NORMAL])
            self.dynaValues[i].CenterOnParent(dir=wx.HORIZONTAL)
            
        #array de tous les sliders
        self.sliders = self.cordSliders + self.tractSliders + self.dynaSliders
        

        """TABLES"""
        self.artiGraph = Grapher(self, xlen=self.artiTable.getSize(), yrange=(0, 1), init=self.artiTable.getPoints(), mode=1, outFunction=self.artiTable.replace)
        self.artiGraph.SetPosition((self.panelSep*2 + self.cordPanelSize[0] + self.tractPanelSize[0] + self.dynaPanelSize[0],50))
        self.artiGraph.SetSize((500, self.dynaPanelSize[1] * 0.5))

        self.ampGraph = Grapher(self, xlen=self.ampTable.getSize(), yrange=(0, 1), init=self.ampTable.getPoints(), mode=0, outFunction=self.ampTable.replace)
        self.ampGraph.SetPosition((self.panelSep*2 + self.cordPanelSize[0] + self.tractPanelSize[0] + self.dynaPanelSize[0], 50 + self.dynaPanelSize[1] * 0.5))
        self.ampGraph.SetSize((500, self.dynaPanelSize[1] * 0.5))
        


        wx.CallAfter(self.showWidgets)
        self.Show()

    def OnSave(self, evt):
        # creation d'un dialogue de sauvegarde
        dlg = wx.FileDialog(self, "Save a preset", style=wx.FD_SAVE)
        # ShowModal() affiche le dialogue et bloque l'execution du programme...
        if dlg.ShowModal() == wx.ID_OK:
            # Si on a appuye sur le bouton SAVE
            # On recupere le path du fichier choisi
            path = dlg.GetPath()
            # On ouvre le fichier en mode ecriture
            f = open(path, "w")
            # On ecrit la liste convertie en string
            f.write(str(self.getValues()))
            # On ferme le fichier
            f.close()
        # Toujours detruire le dialogue
        dlg.Destroy()
        
    def OnLoad(self, evt):
        # creation d'un dialogue de chargement
        dlg = wx.FileDialog(self, "Load a preset", style=wx.FD_OPEN)
        # ShowModal() affiche le dialogue et bloque l'execution du programme...
        if dlg.ShowModal() == wx.ID_OK:
            # Si on a appuye sur le bouton OK
            # On recupere le path du fichier choisi
            path = dlg.GetPath()
            # On ouvre le fichier en mode lecture
            f = open(path, "r")
            # On lit le contenu du fichier (une liste en format string)
            lststr = f.read()
            # On ferme le fichier
            f.close()
            # eval evalue une chaine de caracteres et cree un objet python valide
            lst = eval(lststr)
            # On envoie la liste de frequences au panneau (qui se charge
            # d'ajuster les sliders et les oscillateurs)
            self.setValues(lst)
        # Toujours detruire le dialogue
        dlg.Destroy()

    def getValues(self):
        sliderValues = [self.sliders[i].GetValue() for i in range(len(self.sliders))]
        artValues = self.audio.vocal.envArticulate.getPoints()
        ampValues =  self.audio.vocal.envAmp.getPoints()
        return [sliderValues, artValues, ampValues]

    def setValues(self, lst):
        for i in range(len(lst[0])):
            self.sliders[i].SetValue(lst[0][i])
            evt = wx.PyCommandEvent(wx.EVT_SLIDER.typeId, self.sliders[i].GetId())
            evt.SetEventObject(self.sliders[i])
            evt.SetInt(lst[0][i])
            wx.PostEvent(self.sliders[i].GetEventHandler(), evt)
            
        print lst[1]
        self.audio.vocal.setArticulation(lst[1])
    
    def showWidgets(self):
        # Apres affichage de la fenetre principale, affiche les widgets pyo
        self.audio.vocal.showArticulation()
        self.audio.vocal.showAmplitude()

    def handleServer(self, evt):
        if evt.GetInt() == 1:
            audio.server.start()
            self.serverTog.SetLabel("Stop")
        else:
            audio.server.stop()
            self.serverTog.SetLabel("Start")
            
    def handlePlay(self, evt):
        self.audio.vocal.play()

    """CORDES VOCALES"""
    def handleCordFreq(self, evt):
        x = evt.GetInt() / pow(10, self.cordParams[0][4])
        self.cordValues[0].SetLabel("%.1f" % x)
        self.audio.vocal.setFreq(x)
        
    def handleRipple(self, evt):
        x = evt.GetInt() / pow(10, self.cordParams[1][4])
        self.cordValues[1].SetLabel("%.3f" % x)
        self.audio.vocal.setRipple(x)
        
    def handleWidth(self, evt):
        x = evt.GetInt() / pow(10, self.cordParams[2][4])
        self.cordValues[2].SetLabel("%.2f" % x)
        self.audio.vocal.setWidth(x)
        
    def handleNoisiness(self, evt):
        x = evt.GetInt() / pow(10, self.cordParams[3][4])
        self.cordValues[3].SetLabel("%.3f" % x)
        self.audio.vocal.setNoisiness(x)
       
    """TRACTUS VOCAL"""
    def handleTractBase(self, evt):
        x = evt.GetInt() / pow(10, self.tractParams[0][4])
        self.tractValues[0].SetLabel("%.2f" % x)
        self.audio.vocal.setBase(x)
        
    def handleTractLength(self, evt):
        x = evt.GetInt() / pow(10, self.tractParams[1][4])
        self.tractValues[1].SetLabel("%.3f" % x)
        self.audio.vocal.setLength(x)
        
    def handleTractResonance(self, evt):
        x = evt.GetInt() / pow(10, self.tractParams[2][4])
        self.tractValues[2].SetLabel("%.1f" % x)
        self.audio.vocal.setReson(x)
        
    """DYNAMIQUE"""
    def handleFreqMod(self, evt):
        x = evt.GetInt() / pow(10, self.dynaParams[0][4])
        self.dynaValues[0].SetLabel("%.2f" % x)
        self.audio.vocal.setFreqMod(x)
        
    def handleBaseMod(self, evt):
        x = evt.GetInt() / pow(10, self.dynaParams[1][4])
        self.dynaValues[1].SetLabel("%.2f" % x)
        self.audio.vocal.setBaseMod(x)

    def handleLengthMod(self, evt):
        x = evt.GetInt() / pow(10, self.dynaParams[2][4])
        self.dynaValues[2].SetLabel("%.2f" % x)
        self.audio.vocal.setLengthMod(x)

    def handleResoMod(self, evt):
        x = evt.GetInt() / pow(10, self.dynaParams[3][4])
        self.dynaValues[3].SetLabel("%.2f" % x)
        self.audio.vocal.setResMod(x)

    def handleDur(self, evt):
        x = evt.GetInt() / pow(10, self.dynaParams[4][4])
        self.dynaValues[4].SetLabel("%.2f" % x)
        self.audio.vocal.setDur(x)

            


class Panel(wx.Panel):
    def __init__(self, parent, label, pos, size, color, font=[12, wx.NORMAL, wx.NORMAL]):
        wx.Panel.__init__(self, parent, id=-1, pos=pos, size=size)
        self.SetBackgroundColour(color)
        
        self.label = wx.StaticText(parent=self, label=label)
        self.label.SetFont(wx.Font(font[0], wx.DEFAULT, font[1], font[2]))
        self.label.CenterOnParent(dir=wx.HORIZONTAL)
        
class Slider(wx.Slider):
    def __init__(self, parent, value, min, max, pos, size, handler):
        wx.Slider.__init__(self, parent, id=-1, value=value, minValue=min, maxValue=max, pos=pos, size=size)
        self.Bind(wx.EVT_SLIDER, handler)

class ToggleButton(wx.ToggleButton):
    def __init__(self, parent, pos, label, handler):
        wx.ToggleButton.__init__(self, parent, id=-1, label=label, pos=pos)
        self.Bind(wx.EVT_TOGGLEBUTTON, handler)
        
class Button(wx.Button):
    def __init__(self, parent, pos, label, handler):
        wx.Button.__init__(self, parent, id=-1, label=label, pos=pos)
        self.Bind(wx.EVT_BUTTON, handler)
        
class Label(wx.StaticText):
    def __init__(self, parent, pos=(0,0), text="", font=[12, wx.NORMAL, wx.NORMAL]):
        wx.StaticText.__init__(self, parent, id=-1, label=text, pos=pos)
        self.SetFont(wx.Font(font[0], wx.DEFAULT, font[1], font[2]))


audio = Audio()

app = wx.App(False)

mainFrame = MainFrame(None, title="Vocalizer", pos=(350,0), size=(1400,625), audio=audio)

app.MainLoop()


