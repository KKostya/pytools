import ROOT 
import DataManager
import Bdt
from CutsCollection import *

dm = DataManager.DataManager("..")


bdt = Bdt.Bdt("TT_NL_Mu10",qNoLead+ROOT.TCut("MuPt[0]>10"),dm.Tree("Signal"))
bdt.Train(dm.Tree("Signal"),dm.Tree("TT"),1000,7000)

s  = ROOT.TH1F("s","s",100,0,1)
b  = ROOT.TH1F("b","b",100,0,1)

hsig  = ROOT.TH1F("s","s",20,0,1)
hsig1 = ROOT.TH1F("s","s",40,-1,1)
hbkg  = ROOT.TH1F("b","b",20,0,1)
hbkg1 = ROOT.TH1F("b","b",40,-1,1)

bdt.FillHist(s,dm.Tree("Signal"))
bdt.FillHist(hsig,dm.Tree("Signal"))
bdt.FillHist(hsig1,dm.Tree("Signal"))
bdt.FillHist(b,dm.Tree("TT"))
bdt.FillHist(hbkg,dm.Tree("TT"))
bdt.FillHist(hbkg1,dm.Tree("TT"))

def StyleBkg(h):
    h.SetTitle("BDT output")
    h.Scale(20./dm.Lumi("TT"))
    h.SetStats(ROOT.kFALSE)
    h.SetLineColor(ROOT.kBlack)
    h.SetFillColor(ROOT.kBlack)
    h.SetFillStyle(3004)

def StyleSig(h):
    h.SetTitle("BDT output")
    h.Scale(20./dm.Lumi("Signal"))
    h.SetStats(ROOT.kFALSE)
    h.SetLineColor(ROOT.kRed)
    h.SetFillColor(ROOT.kRed)

StyleBkg(hbkg)
StyleBkg(hbkg1)
StyleBkg(b)
StyleSig(hsig)
StyleSig(hsig1)
StyleSig(s)

c = ROOT.TCanvas("c")

hsig.Draw()
hbkg.Draw("same")

lgnd = ROOT.TLegend(0.8,0.8,1.0,1.0)
lgnd.SetFillColor(ROOT.kWhite)
lgnd.AddEntry(hsig,"Signal","f")
lgnd.AddEntry(hbkg,"TT background","f")

[20.*s.Integral(n,100)/dm.Lumi("Signal") for n in range(10,60,10)] 
[20.*b.Integral(n,100)/dm.Lumi("TT") for n in range(10,60,10)] 



