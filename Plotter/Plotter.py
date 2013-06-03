import ROOT 
from math import sqrt,ceil
from itertools import product,izip,count


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
        self.levels = ['doc','sec','pag','pad']
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
        self.dummy.cd()
        cuttext = ROOT.TPaveText(0.2,0.2,0.8,0.8,"NDC")
        cuttext.AddText(title + ":")
        [cuttext.AddText(t) for t in text]
        cuttext.Draw()
        self.dummy.Print(self.pdfname,"Title: "+title)

    def SetTrees(self, x, level):
        if level not in self.levels raise Exception("Choose a level among: " + str(self.levels))
        self.treeLevel = level
        self.trees = x
    def SetCuts (self,x,level):
        if level not in self.levels raise Exception("Choose a level among: " + str(self.levels))
        self.cuts[level]  = x
    def SetVar  (self,x,level): 
        if level not in self.levels raise Exception("Choose a level among: " + str(self.levels))
        self.varLevel = level 
        self.vrbls = x

    def Draw(self,tree,title,cuts,data,norms={}):
        localGC=[]

        data = {}
        for l in self.levels:
            data[l]=[]
            if self.treeLevel == l: data[l].append(self.trees)
            if l in self.cuts:      data[l].append(self.cuts[l])
            if self.varLevel  == l: data[l].append(self.vrbls)

        # 2DO -- this. Log, nostack options, statspad
        #
        # class data:
        #     def __new__(self): 
        #         cuts = [] 
        #         tree = None
        #         var  = None
        #         options = []
        #     def process(d):
        #         ttl = []  
        #         if  'tree' in d: tree = d['tree']
        #         if   'cut' in d: cuts.append(d['cut'])
        #         if   'var' in d: var = d['var']
        #         if 'title' in d: ttl.append(d['title'])
        #         return ','.join(ttl)                

        cuts = [] 
        tree = None
        var  = None
        for docdat in product(*data[self.levels[0]]):
            # Process sections 
            sectitle, sectext = [],[]
            for d in docdat: 
                if  'tree' in d: tree = d['tree']
                if   'cut' in d: cuts.append(d['cut'])
                if   'var' in d: var = d['var']
                if 'title' in d: sectitle.append(d['title'])
                if  'text' in d: sectext.append( d['text'])
            self.PaveText(','.join(sectitle), sectext)

            for secdat in product(*data[self.levels[1]]):
                # Process pages
                pgtitle = []
                for d in secdat:
                    if  'tree' in d: tree = d['tree']
                    if   'cut' in d: cuts.append(d['cut'])
                    if   'var' in d: var = d['var']
                    if 'title' in d: pgtitle.append(d['title'])

                # finding number of pads and number of legend entries
                npads = 1; for x in data[self.levels[2]]: npads *= len(x)
                nlgnd = 1; for x in data[self.levels[3]]: nlgnd *= len(x)

                self.setupPad   (','.join(pgtitle),npads)
                self.setupLegend(nlgnd)

                for pagdat,npad in izip(product(*data[self.levels[2]]),count(1)):
                    # Process pads
                    self.pad.cd(npad)
                    padtitle = []
                    for d in pagdat:
                        if  'tree' in d: tree = d['tree']
                        if   'cut' in d: cuts.append(d['cut'])
                        if   'var' in d: var = d['var']
                        if 'title' in d: padtitle.append(d['title'])

                    # Creating histogram stack
                    hstack = ROOT.THStack("hs",','.join(padtitle))
                    localGC.append(hstack)

                    for paddat,nh in izip(product(*data[self.levels[3]]),count(0)):
                        # Processing histograms 
                        htitle = []
                        color = nh
                        for d in paddat:
                            if  'tree' in d: tree = d['tree']
                            if   'cut' in d: cuts.append(d['cut'])
                            if   'var' in d: var = d['var']
                            if 'title' in d: htitle.append(d['title'])
                            if 'color' in d: color = d['color'] 
                        #Payback time here:
                        if  var == None: raise Exception("No variables were selected")
                        if tree == None: raise Exception("No trees were provided")
                        
                        hname = "htemp"+str(nh)
                        hist = ROOT.TH1F(hname,"No title",var['nbins'],var['min'],var['max']) 
                        hstack.Add(hist)
                        localGC.append(hist)

                        hist.SetStats(ROOT.kFALSE)
                        hist.SetFillColor(color)
                        hist.SetMarkerColor(color if color!=ROOT.kWhite else ROOT.kBlack)
                        hist.SetLineColor(ROOT.kBlack)
                        tree.Draw(func+">>"+hname, '&&'.join(["("+c+")" for c in cuts])

                        self.lentries[nh].SetObject(hist)
                        self.lentries[nh].SetLabel(','.join(htitle))

                    hstack.Draw("")

                self.canv.Print(self.pdfname,"Title: " + ','.join(pgtitle)) 



    def Finish(self):
        self.canv.Print(self.pdfname+"]")



                                    


