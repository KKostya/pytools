import ROOT 
from math import sqrt,ceil
from itertools import product,izip,count




def DrawHistogram(data,nh):
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
    hist.SetFillColor(data.color)
    hist.SetMarkerColor(data.color if data.color!=ROOT.kWhite else ROOT.kBlack)
    hist.SetLineColor(ROOT.kBlack)
    data.tree.Draw(data.var[0]+">>"+hname, '&&'.join(["("+c+")" for c in data.cuts if c]))

    data.lentry.SetObject(hist)
    data.lentry.SetLabel(data.title)

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
        self.decorators =  { 'pad': self.HistLoop, 
                             'pag': self.PadLoop, 
                             'sec': self.PageLoop, 
                             'doc': self.SectLoop  }
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
                self.tree = None
                self.var  = None
                self.GC = []
            def Fill(self, dat, title, cuts):
                for d in dat: 
                    if  'tree' in d:  self.tree = d['tree']
                    if   'var' in d:  self.var  = d['var']
                    if 'title' in d: title.append(d['title'])
                    if   'cut' in d:  cuts.append(d['cut'])
        dt = Data()

        # TODO Log and nostack options, statspad, normalization, weightexpr

        f = DrawHistogram
        for l in self.levels:
            data=[]
            if self.treeLevel == l: data.append(self.trees)
            if l in self.cuts:      data.append(self.cuts[l])
            if self.varLevel  == l: data.append(self.vrbls)
            f = self.decorators[l](f,data)
        f(dt,0)


    def HistLoop(self,f,pdat):
        def ret(dt,idx):
            # Creating legend
            nlgnd = 1
            for x in pdat: nlgnd *= len(x)
            self.setupLegend(nlgnd)
            # Looping
            self.pad.cd(idx)
            for paddat,nh in izip(product(*pdat),count(0)):
                # Processing histograms 
                htitle, dt.cuts = [], dt.padcut[:]
                dt.color = nh+2
                dt.Fill(paddat,htitle,dt.cuts)
                for d in paddat: 
                    if 'color' in d: dt.color = d['color']
                dt.lentry = self.lentries[nh]
                dt.title  = ','.join(htitle)
                f(dt,nh)
        return ret

    def PadLoop(self,f,pgdat):
        def ret(dt,idx):
            # Creating Pads
            npads = 1
            for x in pgdat: npads *= len(x)
            self.setupPad(','.join(dt.pgtitle),npads)
            # Looping
            for pagdat,npad in izip(product(*pgdat),count(1)):
                # Process pads
                self.pad.cd(npad)
                padtitle  = []
                dt.padcut = dt.pgcut[:]
                dt.Fill(pagdat,padtitle,dt.padcut)
                # Creating histogram stack
                dt.hstack = ROOT.THStack("hs",','.join(padtitle))
                dt.GC.append(dt.hstack)
                f(dt,npad)
                dt.hstack.Draw("nostack")
        return ret

    def PageLoop(self,f,scdat):
        def ret(dt,idx):
            for secdat,npage in izip(product(*scdat),count()):
                # Process pages
                dt.pgtitle = [] 
                dt.pgcut   = dt.seccut[:]
                dt.Fill(secdat,dt.pgtitle,dt.pgcut)
                f(dt,npage)
                self.canv.Print(self.pdfname,"Title: " + ','.join(dt.pgtitle)) 
        return ret

    def SectLoop(self,f,dcdat):
        def ret(dt,idx):
            for docdat,nsec in izip(product(*dcdat),count()):
                # Process sections 
                sectitle, sectext, dt.seccut = [],[],[]
                dt.Fill(docdat,sectitle,dt.seccut)
                for d in docdat: 
                    if 'text' in d: sectext += d['text']
                self.PaveText(','.join(sectitle), sectext)
                f(dt,nsec) 
        return ret

    def Finish(self):
        self.canv.Print(self.pdfname+"]")



                                    


