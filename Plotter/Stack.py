import ROOT 
from math import sqrt,ceil


gcSave = []
class StackPlotter:
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


    def Draw(self,tree,title,cuts,data,norms={}):
        localGC=[]

        normfactor = 1
        if "cs" and "lumi" in norms:
            normfactor = norms["cs"] * norms["lumi"] / tree.GetEntries()

        # Graphics setup
        self.setupPad(title,len(data))        
        self.setupLegend(len(cuts))        

        # Processing
        npad = 0
        for hTitle,ranges,func,options in data:
            npad += 1
            self.pad.cd(npad)
            # Setting log options
            ROOT.gPad.SetLogx(ROOT.kTRUE if 'LogX' in options else ROOT.kFALSE)
            ROOT.gPad.SetLogy(ROOT.kTRUE if 'LogY' in options else ROOT.kFALSE)

            # Creating histogram stack
            hstack = ROOT.THStack("hs",hTitle)
            localGC.append(hstack)

            # Adding 'stats' pad
            stats = self.StatsPad(norms["title"] if "title" in norms else "Events:",normfactor)
            localGC.append(stats)

            # Processing cuts
            nh = 0
            for cut,ltitle,color in cuts:
                hname = "htemp"+str(nh)
                hist = ROOT.TH1F(hname,hTitle,ranges[0],ranges[1],ranges[2]) 
                hstack.Add(hist)
                localGC.append(hist)

                hist.SetStats(ROOT.kFALSE)
                hist.SetFillColor(color)
                hist.SetMarkerColor(color if color!=ROOT.kWhite else ROOT.kBlack)
                hist.SetLineColor(ROOT.kBlack)
                tree.Draw(func+">>"+hname, cut)

                self.lentries[nh].SetObject(hist)
                self.lentries[nh].SetLabel(ltitle)

                stats.AddCount(hist.GetEntries(),color)

                nh += 1
            hstack.Draw("nostack" if 'NoStack' in options else "")
            stats.Draw()
        self.canv.Print(self.pdfname,"Title: " + title) 


    def Finish(self):
        self.canv.Print(self.pdfname+"]")
