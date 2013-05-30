import ROOT 
from math import sqrt,ceil


gcSave = []
class PerCutPlotter:
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
        # Creatin empty cnavas for
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

    def PaveText(self,title,text):
        self.dummy.cd()
        cuttext = ROOT.TPaveText(0.2,0.2,0.8,0.8,"NDC")
        cuttext.AddText(title + ":")
        [cuttext.AddText(t) for t in text]
        cuttext.Draw()
        self.dummy.Print(self.pdfname,"Title: "+title)


    def Draw(self,tree,func,range,title,data,norms={}):
        localGC=[]

	normfactor = 1
	if "cs" and "lumi" in norms:
	    normfactor = norms["cs"] * norms["lumi"] / tree.GetEntries()

        # Graphics setup
        self.setupPad(title,len(data))        

        # Processing
        npad = 0
        for hTitle,cut,options in data:
            npad += 1
            self.pad.cd(npad)
            # Setting log options
            ROOT.gPad.SetLogx(ROOT.kTRUE if 'LogX' in options else ROOT.kFALSE)
            ROOT.gPad.SetLogy(ROOT.kTRUE if 'LogY' in options else ROOT.kFALSE)

            # Adding 'stats' pad
            stats = self.StatsPad(norms["title"] if "title" in norms else "Events:",normfactor)
            localGC.append(stats)

            hname = "htemp"+str(npad)
            hist = ROOT.TH1F(hname,hTitle,range[0],range[1],range[2]) 
            hist.SetStats(ROOT.kFALSE)
            hist.SetFillColor(ROOT.kBlue)
            hist.SetLineColor(ROOT.kBlack)
            localGC.append(hist)
            
            tree.Draw(func+">>"+hname, cut)
            hist.Draw("")

            stats.AddCount(hist.GetEntries(),ROOT.kBlack)
            stats.Draw()

        self.canv.Print(self.pdfname,"Title: " + title) 

    def Finish(self):
        self.canv.Print(self.pdfname+"]")
