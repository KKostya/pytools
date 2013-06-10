import ROOT 
from itertools import product,groupby,izip,count,tee
from math import sqrt,ceil
from copy import copy

#TODO treat titles as cuts -- same cathegory combines them

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
        ret.data = []
        for s,o in product(self.data,other.data):
            dct = dict(s.items() + o.items())
            # Special treatment for cuts
            if other.t == self.t:
                if ((self.t,'cut') in s) and ((self.t,'cut') in o):
                    print "Product cuts"
                    dct[(self.t,'cut')] = "({0})&&({1})".format(s[(self.t,'cut')],o[(self.t,'cut')])
            ret.data.append(dct)
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

#http://stackoverflow.com/questions/480214/how-do-you-remove-duplicates-from-a-list-in-python-whilst-preserving-order
#http://stackoverflow.com/questions/6280978/how-to-uniqify-a-list-of-dict-in-python
#http://stackoverflow.com/questions/5844672/delete-an-element-from-a-dictionary
def group(seq, key):
    seen = set()
    seen_add = lambda x: seen.add(tuple(x.items()))
    ukeys = [ x[key] for x in seq if tuple(x[key].items()) not in seen and not seen_add(x[key])]
    ret = []
    for k in ukeys:
        grp = []
        for x in seq:
            if x[key] != k: continue
            dcp = dict(x)
            del dcp[key]
            grp.append(dcp)
        ret.append((k,grp))
    return ret

class Product(Plotter):
    def __init__(self,p1,p2):
        self.t = tuple(sorted([p1.t,p2.t]))

    def Transpose(self):
        # Start with transpositions
        tr = []
        for datum in self.data:
            dic = {}
            for k in datum:
                if k[0] not in dic: dic[k[0]] = {}
                dic[k[0]][k[1]] = datum[k] 
            tr.append(dic)
        a = []
        for secset, scgrp in group(tr,'sec'):
            b = []
            for pagset, pggrp in group(scgrp,'page'):
                c = []
                for padset, pdgrp in  group(pggrp,'pad'):
                    d = []
                    for histset, hsgrp in group(pdgrp,'hist'):
                        d.append((histset,hsgrp))
                    c.append((padset,d))
                b.append((pagset,c))
            a.append((secset,b))
        return a

    def Draw(self, pdfname):
        GC = []
        plt = PlotUtil(pdfname)
        dt = self.Transpose()
        for secset, scgrp in dt:
            print secset
            plt.PaveText(secset.get("title",""),secset.get('text',[]))
            for pagset, pggrp in scgrp:
                print "  ",pagset
                # Creating pads
                npads = len(pggrp)
                pageTitle = pagset['title'] if 'title' in pagset else "No title"
                plt.setupPad(pageTitle,npads)
                for (padset, pdgrp),npad in izip( pggrp, count()):
                    print "    ",padset
                    # Creating legend
                    nlgnd = len(pdgrp)
                    plt.setupLegend(nlgnd)
                    # Creating histogram stack
                    plt.pad.cd(npad+1)
                    hstack = ROOT.THStack("hs",padset['title'] if 'title' in padset else "")
                    GC.append(hstack)
                    for (histset, hsgrp),nh in izip(pdgrp, count()):
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
                                cutstr = "{0}*({1})".format(settings['weight'],cutstr if cutstr else "1>0")
                        # Making histogram
                        hname = "htemp"+str(nh)
                        hist = ROOT.TH1F(hname,"No title",settings['var'][1],settings['var'][2],settings['var'][3]) 
                        hstack.Add(hist)
                        GC.append(hist)
                        # Set more options
                        hist.SetStats(ROOT.kFALSE)
                        if 'fill' in settings: hist.SetFillColor(settings['fill'])
                        hist.SetLineColor(settings['color'] if 'color' in settings else ROOT.kBlack)
                        hist.SetMarkerColor(settings['color'] if 'color' in settings else ROOT.kBlack)
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



                                    


