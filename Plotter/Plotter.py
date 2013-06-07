import ROOT 
from math import sqrt,ceil
from itertools import product,izip,count



class HistogramDrawer:
    def Run(self,data,nh):
        #  Assertions
        #Payback time here
        if data.var  == None: raise Exception("No variables were selected")
        if data.tree == None: raise Exception("No trees were provided")
        # Plotting
        hname = "htemp"+str(nh)
        hist = ROOT.TH1F(hname,"No title",data.var[1],data.var[2],data.var[3]) 
        data.hstack.Add(hist)
        data.GC.append(hist)

        hist.SetStats(ROOT.kFALSE)
        if data.fill: hist.SetFillColor(data.fill)
        hist.SetLineColor(data.color if data.color else ROOT.kBlack)
        hist.SetMarkerColor(data.color if data.color else ROOT.kBlack)

        cutstr = '&&'.join(["("+c+")" for c in data.cuts if c])
        if data.weight: cutstr = "{0}*({1})".format(data.weight,cutstr)

        data.tree.Draw(data.var[0]+">>"+hname, cutstr)

        data.lentry.SetOption("f" if data.fill else "l")
        data.lentry.SetObject(hist)
        data.lentry.SetLabel(data.GetTitle())

class Looper:
    def SetData(self,data):
        self.data = data
    def SetInner(self,inn):
        self.innerLoop = inn

class HistLoop(Looper):
    def Run(self,dt,idx):
        print "   Hist Loop"
        # Creating legend
        nlgnd = 1
        for x in self.data: nlgnd *= len(x)
        dt.plotter.setupLegend(nlgnd)
        # Creating histogram stack
        dt.plotter.pad.cd(idx)
        dt.hstack = ROOT.THStack("hs",dt.GetTitle())
        dt.GC.append(dt.hstack)
        for paddat,nh in izip(product(*self.data),count(0)):
            # Processing histograms 
            htitle, dt.cuts = [], dt.padcut[:]
            dt.Fill(paddat,dt.cuts)
            for d in paddat: 
                if 'color' in d: dt.color = d['color']
            dt.lentry = dt.plotter.lentries[nh]
            self.innerLoop.Run(dt,nh)
        dt.hstack.Draw("nostack")

class PadLoop(Looper):
    def Run(self,dt,idx):
        print "  Pad Loop"
        # Creating Pads
        npads = 1
        for x in self.data: npads *= len(x)
        pageTitle = dt.GetTitle()
        dt.plotter.setupPad(pageTitle,npads)
        # Looping
        for pagdat,npad in izip(product(*self.data),count(1)):
            dt.padcut = dt.pgcut[:]
            dt.Fill(pagdat,dt.padcut)
            self.innerLoop.Run(dt,npad)
        dt.plotter.canv.Print(dt.plotter.pdfname,"Title: " + pageTitle) 

class PageLoop(Looper):
    def Run(self,dt,idx):
        print " Page Loop"
        for secdat,npage in izip(product(*self.data),count()):
            # Process pages
            dt.pgcut   = dt.seccut[:]
            dt.Fill(secdat,dt.pgcut)
            self.innerLoop.Run(dt,npage)

class SectLoop(Looper):
    def Run(self,dt,idx):
        print "Section Loop"
        for docdat,nsec in izip(product(*self.data),count()):
            # Process sections 
            sectext, dt.seccut = [],[]
            dt.Fill(docdat,dt.seccut)
            for d in docdat: 
                if 'text' in d: sectext += d['text']
            dt.plotter.PaveText(dt.GetTitle(), sectext)
            self.innerLoop.Run(dt,nsec) 

class ListLoop(Looper):
    def Run(self,dt,idx):
        print "-------"
        databack = self.innerLoop.data[:]
        for lstdat in self.data:
            self.innerLoop.data = databack + [lstdat]
            self.innerLoop.Run(dt,idx) 
        self.innerLoop.data = databack

gcSave = []
class Plotter:
    # Inner class for stats printing
    class StatsPad:
        def __init__(self,title,norm):
            self.norm = norm
            self.pave =  ROOT.TPaveText(0.65,0.65,0.8,0.8,"NDC")
            self.pave.SetFillColor(ROOT.kWhite)
            self.pave.SetBorderSize(1)
            self.pave.SetTextAlign(22)
            self.pave.AddText(title)
        def AddCount(self,count,color):
            txt = self.pave.AddText("%g" % (count * self.norm))
            txt.SetTextColor(color if color!=ROOT.kWhite else ROOT.kBlack)
        def Draw(self): self.pave.Draw()

    # Main class
    def __init__(self,pdfname):
        # General information

        self.levels = ['pad','pag','sec','doc']
        self.loopers =     { 'pad': HistLoop(), 
                             'pag': PadLoop() , 
                             'sec': PageLoop(), 
                             'doc': SectLoop()  }
        self.cuts = {}


        # Creatin empty canvas for
        self.dummy = ROOT.TCanvas()
        # Creating main canvas
        self.canv     = ROOT.TCanvas( "canv"  , "Spectra")
        self.titlepad = ROOT.TPad   ( "title" , "",0,0.9,1,1)
        self.titlepad.Draw()

        # Creating title
        self.titlepad.cd()
        self.title = ROOT.TText(0.5,0.5,"")
        self.title.SetTextSize(0.5)
        self.title.SetTextAlign(22)
        self.title.Draw()
        
        # Creating main pad
        self.canv.cd()
        self.pad = ROOT.TPad("histos","",0,0,1,0.9)
        self.pad.Draw()

        # Preparing pdf file
        self.pdfname = pdfname
        self.canv.Print(self.pdfname+"[") 

    def setupPad(self,title,ndiv):
        # Setting title
        self.title.SetText(0.5,0.5,title)
        self.titlepad.cd()
        self.title.Draw()

        # Dividing the main pad
        self.pad.Clear()
        ny = int(sqrt(ndiv+1.2)) 
        self.pad.Divide(int(ceil(float(ndiv)/ny)),ny)

    def setupLegend(self,num):
        self.titlepad.cd()
        self.lgnd = ROOT.TLegend(0.8,0.0,1.0,1.0)
        self.lgnd.SetFillColor(ROOT.kWhite)
        self.lentries = [self.lgnd.AddEntry(self.dummy,"","f") for i in range(num)] 
        self.lgnd.Draw()

    def PaveText(self,title,text):
        if not title: title = "No title"
        self.dummy.cd()
        cuttext = ROOT.TPaveText(0.2,0.2,0.8,0.8,"NDC")
        cuttext.AddText(title + ":")
        if text: [cuttext.AddText(t) for t in text]
        cuttext.Draw()
        self.dummy.Print(self.pdfname,"Title: "+title)

    def SetTrees(self, x, level):
        if level not in self.levels: raise Exception("Choose a level among: " + str(self.levels))
        self.treeLevel = level
        self.trees = x
    def SetCuts (self,x,level):
        if level not in self.levels: raise Exception("Choose a level among: " + str(self.levels))
        self.cuts[level]  = x
    def SetVars (self,x,level): 
        if level not in self.levels: raise Exception("Choose a level among: " + str(self.levels))
        self.varLevel = level 
        self.vrbls = x

    def Draw(self):
        localGC=[]

        # Utility class that manages data across levels
        class Data:
            def __init__(self):
                self.title = ""
                self.tree    = None
                self.var     = None
                self.weight  = None
                self.fill    = None
                self.color   = None
                self.GC = []
            def Fill(self, dat, cuts):
                listTitle = [self.title] if self.title else []
                for d in dat: 
                    if   'fill' in d:  self.fill   = d[  'fill']
                    if  'color' in d:  self.color  = d[ 'color']
                    if 'weight' in d:  self.weight = d['weight']
                    if   'tree' in d:  self.tree   = d[  'tree']
                    if    'var' in d:  self.var    = d[   'var']
                    if  'title' in d:  listTitle.append(d['title'])
                    if    'cut' in d:  cuts.append(d['cut'])
                self.title =','.join(listTitle)
            def GetTitle(self):
                ret = self.title
                self.title = ""
                return ret

        dt = Data()
        dt.plotter = self

        # TODO Log and nostack options, statspad, normalization, weightexpr

        f = HistogramDrawer()
        for l in self.levels:
            data=[]
            if self.treeLevel == l: data.append(self.trees)
            if l in self.cuts:      data.append(self.cuts[l])
            if self.varLevel  == l: 
                if isinstance(self.vrbls[0],list):
                    listlooper = ListLoop()
                    listlooper.SetData(self.vrbls)
                    listlooper.SetInner(f)
                    f = listlooper 
                else: data.append(self.vrbls)
            looper = self.loopers[l]
            looper.SetData(data)
            looper.SetInner(f)
            f = looper 
        f.Run(dt,0)

    def Finish(self):
        self.canv.Print(self.pdfname+"]")



                                    


