import ROOT,array

#  Example1:
#  import BandGraph
#  bgr=BandGraph.BandGraph(range(10),[x/2. for x in range(10)], range(10), [2.*x for x in range(10)])
#  bgr.Draw("A")

#  Example2 (http://root.cern.ch/root/html/tutorials/graphics/graphShade.C.html):
#  import BandGraph, math
#  xs = [ i/10. for i in range(20)]
#  bgr  = BandGraph.BandGraph(xs,
#           [ 8.*math.sin(x+0.1 ) for x in xs], 
#           [ 9.*math.sin(x+0.15) for x in xs],
#           [10.*math.sin(x+0.2 ) for x in xs])
#  bgr.SetLineWidth(4);
#  bgr.SetMarkerColor(4);
#  bgr.SetMarkerStyle(21);
#  bgr.Draw("CP")

class BandGraph:
    def __init__(self, xs ,mins, cnts, maxs):
        n = len(xs)
        if any([n != len(maxs), n != len(mins), n != len(cnts)]) : 
            raise Exception("BandGraph inputs must be of the same length.")

        self.arrxs  = array.array('f',xs)

        self.arrmin = array.array('f',mins); self.tgrmin = ROOT.TGraph(n, self.arrxs, self.arrmin) 
        self.arrcnt = array.array('f',cnts); self.tgrcnt = ROOT.TGraph(n, self.arrxs, self.arrcnt) 
        self.arrmax = array.array('f',maxs); self.tgrmax = ROOT.TGraph(n, self.arrxs, self.arrmax) 

        self.tgrarea = ROOT.TGraph(2*n)
        for i in range(n):
            self.tgrarea.SetPoint(  i,xs[i],    maxs[i])
            self.tgrarea.SetPoint(n+i,xs[n-i-1],mins[n-i-1])

        self.tgrarea.GetHistogram().SetMinimum(min(mins))
        self.tgrarea.GetHistogram().SetMaximum(max(maxs))
                
        self.SetFillStyle(3013)
        self.SetFillColor(16)
        self.SetLineWidth(2)

    def SetMinMax(self,mi,ma):
        self.tgrarea.GetHistogram().SetMinimum(mi)
        self.tgrarea.GetHistogram().SetMaximum(ma)
                
    def SetTitle(self,t): self.tgrarea.SetTitle(t)
    def SetFillStyle(self,s):self.tgrarea.SetFillStyle(s)
    def SetFillColor(self,c):self.tgrarea.SetFillColor(c)
    def SetLineWidth(self,w):self.tgrcnt.SetLineWidth(w)
    def SetLineColor(self,c):self.tgrcnt.SetLineColor(c)
    def SetMarkerColor(self,c): self.tgrcnt.SetMarkerColor(c)
    def SetMarkerStyle(self,s): self.tgrcnt.SetMarkerStyle(s)
    def SetExtLineWidth(self,w):
        tgrmin.SetLineWidth(w)
        tgrmax.SetLineWidth(w)
    def SetExtLineColor(self,c):
        tgrmin.SetLineColor(c)
        tgrmax.SetLineColor(c)

    def Draw(self, opts=""):
        self.tgrarea.Draw('Af' if 'A' in opts else 'f')
        self.tgrmin.Draw('l')
        self.tgrmax.Draw('l')
        self.tgrcnt.Draw(opts.strip('A'))
