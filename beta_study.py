import ROOT 

import RootTools.DataManager

dm = RootTools.DataManager.DataManager("..")
sig = dm.Tree("Signal")

from RootTools import CutsCollection

from RootTools.Plotter import Stack

plotter = Stack("BetaPlots.pdf")

def DrawHists(title,hc):
    cfg = ""
    for h,c in hc:
        h.SetTitle(title)
        h.SetStats(ROOT.kFALSE)
        h.SetLineColor(ROOT.kBlack)
        h.SetLineWidth(2)
        h.SetFillColor(c)
        h.Draw(cfg)
        cfg = "same"

gc=[]
printpdf = "BetaStudy.pdf"
canv = ROOT.TCanvas("canv","Spectra")
canv.Print(printpdf+"[")


for nm in dm.Names():
        h = [ROOT.TH1F("h"+str(i),"h"+str(i),100,0,1) for i in range(3)]
        gc += h
        for i,l in zip(range(3),["L","M","T"]):
                dm.Tree(nm).Draw("JetpuBeta[{0}]>>h{1}".format("ICSV{0}[0]".format(l),i))

        DrawHists(nm,zip(h,[ROOT.kBlue,ROOT.kGreen,ROOT.kRed]))
        canv.Print(printpdf,"Title:"+nm)

canv.Print(printpdf+"]")
