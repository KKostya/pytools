import ROOT 
from itertools import product,groupby,izip,count,tee
from math import sqrt,ceil
from copy import copy

class Plotter(object):
    def __init__(self, **args):
        dic = {}
        for k in args: dic[(self.t,k)] = args[k]
        self.data = [dic]

    def __add__(self, other):
        if other.t != self.t: 
            raise TypeError("You cannot connect (with \"+\") {0} and {1}".format(self.t,other.t))
        ret = copy(self)
        ret.data = self.data + other.data
        return ret

    def __mul__(self, other):
        ret = copy(self) if other.t == self.t else Product(self,other)
        ret.data = [dict(s.items() + o.items()) for s,o in product(self.data,other.data)]
        return ret

class Hist(Plotter):
    def __init__(self,**args):
        self.t = "hist" 
        super(Hist,self).__init__(**args)

class Pad(Plotter):
    def __init__(self,**args):
        self.t = "pad" 
        super(Pad,self).__init__(**args)

class Page(Plotter):
    def __init__(self,**args):
        self.t = "page" 
        super(Page,self).__init__(**args)

class Sec(Plotter):
    def __init__(self,**args):
        self.t = "sec" 
        super(Sec,self).__init__(**args)

class Product(Plotter):
    def __init__(self,p1,p2):
        self.t = tuple(sorted([p1.t,p2.t]))

    def Transpose(self):
        ret = []
        for datum in self.data:
            dic = {}
            for k in datum:
                if k[0] not in dic: dic[k[0]] = {}
                dic[k[0]][k[1]] = datum[k] 
            ret.append(dic)
        return ret

    def Draw(self, pdfname):
        GC = []
        plt = PlotUtil(pdfname)
        dt = self.Transpose()
        
        for secset, scgrp in groupby(dt, lambda x: x['sec']):
            print secset
            plt.PaveText(secset.get("title",""),secset.get('text',[]))
            for pagset, pggrp in groupby(scgrp, lambda x: x['page']):
                print "  ",pagset
                # Creating pads
                pggrp, temp = tee(pggrp)
                npads = len(list(groupby(temp, lambda x: x['pad'])))
                pageTitle = pagset['title'] if 'title' in pagset else "No title"
                plt.setupPad(pageTitle,npads)
                for (padset, pdgrp),npad in izip( groupby(pggrp, lambda x: x['pad']), count()):
                    print "    ",padset
                    # Creating legend
                    pdgrp, temp = tee(pdgrp)
                    nlgnd = len(list(temp))
                    plt.setupLegend(nlgnd)
                    # Creating histogram stack
                    plt.pad.cd(npad+1)
                    hstack = ROOT.THStack("hs",padset['title'] if 'title' in padset else "")
                    GC.append(hstack)
             
                    for (histset, hsgrp),nh in izip( groupby(pdgrp, lambda x: x['hist']), count()):
                        print "       ",histset
                        # Condensing plot data
                        diclst = [] 
                        for s in [secset,pagset,padset,histset]: diclst += s.items()
                        settings = dict(diclst)
                        # Cuts need special treatment
                        cuts = []
                        for s in [secset,pagset,padset,histset]: 
                            if 'cut' in s: 
                                if s['cut']:
                                    cuts.append("({0})".format(s['cut']))
                        cutstr = '&&'.join(cuts)
                        if 'weight' in settings: 
                            if settings['weight']: 
                                cutstr = "{0}*({1})".format(settings['weight'],cutstr)
                        # Making histogram
                        hname = "htemp"+str(nh)
                        hist = ROOT.TH1F(hname,"No title",settings['var'][1],settings['var'][2],settings['var'][3]) 
                        hstack.Add(hist)
                        GC.append(hist)
                        # Set more options
                        hist.SetStats(ROOT.kFALSE)
                        if 'fill' in settings: hist.SetFillColor(settings['fill'])
                        hist.SetLineColor('color' if 'color' in settings else ROOT.kBlack)
                        hist.SetMarkerColor('color' if 'color' in settings else ROOT.kBlack)
                        # Drawing 
                        settings['tree'].Draw(settings['var'][0]+">>"+hname, cutstr)
                        # Processing legend
                        plt.lentries[nh].SetOption("f" if 'fill' in settings else "l")
                        plt.lentries[nh].SetObject(hist)
                        plt.lentries[nh].SetLabel(settings['title'] if 'title' in settings else "")
                    hstack.Draw("nostack")
                plt.canv.Print(pdfname,"Title: " + pageTitle) 
        plt.Finish()

# TODO: Understand whats wrong with friggin GC
globGC = []
class PlotUtil(object):
    def __init__(self,pdfname):
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

        globGC.append(self.canv) 
        globGC.append(self.pad) 
        globGC.append(self.titlepad) 

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

    def Finish(self):
        self.canv.Print(self.pdfname+"]")



                                    


