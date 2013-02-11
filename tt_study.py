import ROOT 

import DataManager
dm = DataManager.DataManager("..")

############################### Input data #########################################
lumi = 20.

from RooFuncs import MakeInvm,Register,SumP4
sig = dm.Tree("Signal")
MakeInvm(sig,"Mmm",["Mu","Mu"],["[0]","[1]"])
MakeInvm(sig,"Mbb",["BJet","BJet"],["[0]","[1]"])
MakeInvm(sig,"Mmmbb",["BJet","BJet","Mu","Mu"],["[0]","[1]","[0]","[1]"])
MakeInvm(sig,"Mjj",["Jet","Jet"],["[0]","[1]"])
MakeInvm(sig,"Mmmjj",["Jet","Jet","Mu","Mu"],["[0]","[1]","[0]","[1]"])

MakeInvm(sig,"gMmm",["GenMu","GenMu"],["[0]","[1]"])
MakeInvm(sig,"gMee",["GenE","GenE"],["[0]","[1]"])
MakeInvm(sig,"gMbb",["GenB","GenB"],["[0]","[1]"])


Register(sig,"SumPxB" , SumP4(["Mu","Mu","BJet","BJet"],["[0]","[1]","[0]","[1]"])[1])
Register(sig,"SumPyB" , SumP4(["Mu","Mu","BJet","BJet"],["[0]","[1]","[0]","[1]"])[2])
Register(sig,"SumPtB" , "sqrt(SumPxB^2+SumPyB^2)")

Register(sig,"SumPx" , SumP4(["Mu","Mu","Jet","Jet"],["[0]","[1]","[0]","[1]"])[1])
Register(sig,"SumPy" , SumP4(["Mu","Mu","Jet","Jet"],["[0]","[1]","[0]","[1]"])[2])
Register(sig,"SumPt" , "sqrt(SumPx^2+SumPy^2)")

Register(sig,"DRbm11" , "sqrt((MuPhi[0]-BJetPhi[0])^2+(MuEta[0]-BJetEta[0])^2)")
Register(sig,"DRbm12" , "sqrt((MuPhi[0]-BJetPhi[1])^2+(MuEta[0]-BJetEta[1])^2)")
Register(sig,"DRbm21" , "sqrt((MuPhi[1]-BJetPhi[0])^2+(MuEta[1]-BJetEta[0])^2)")
Register(sig,"DRbm22" , "sqrt((MuPhi[1]-BJetPhi[1])^2+(MuEta[1]-BJetEta[1])^2)")
 
Register(sig,"DRjm11" , "sqrt((MuPhi[0]-JetPhi[0])^2+(MuEta[0]-JetEta[0])^2)")
Register(sig,"DRjm12" , "sqrt((MuPhi[0]-JetPhi[1])^2+(MuEta[0]-JetEta[1])^2)")
Register(sig,"DRjm21" , "sqrt((MuPhi[1]-JetPhi[0])^2+(MuEta[1]-JetEta[0])^2)")
Register(sig,"DRjm22" , "sqrt((MuPhi[1]-JetPhi[1])^2+(MuEta[1]-JetEta[1])^2)")
 
######################################################################################
gcDat = []
canv = ROOT.TCanvas("HZZ Plot")

########################## Cuts #########################33
from CutsCollection import *

def evts(c):
    names = dm.Names()
    nums = [dm.Tree(n).Draw("JetPt@.size()",c) for n in names]
    return [(name , num*lumi/dm.Lumi(name), num) for name,num in zip(names,nums)]
#
#def draw(f,rng,c):
#    global gcDat
#    hsts = [ROOT.TH1F(n,n,rng[0],rng[1],rng[2]) for n,a,b,co in ntData] 
#    gcDat += hsts
#    nums = [t.Draw(f+">>"+n,c) for n,b,t,co in trees]
#    same = False 
#    for (tit, cs, tree,color), num, h in zip(trees,nums,hsts):
#         if not(h.Integral() == 0): h.Scale(cs * lumi * float(num)/(tree.GetEntries()*h.Integral()))
#	 h.SetLineColor(color)
#	 h.Draw("same" if same else "")
#         same = True 
#
#def drawS(f,rng,c):
#    global gcDat
#    hsts = [ROOT.TH1F(n,n,rng[0],rng[1],rng[2]) for n,a,b,co in ntData] 
#    gcDat += hsts
#    nums = [t.Draw(f+">>"+n,c) for n,b,t,co in trees]
#    same = False 
#    for (tit, cs, tree,color), num, h in zip(trees,nums,hsts):
#         if not(h.Integral() == 0): h.Scale(1/h.Integral())
#	 h.SetLineColor(color)
#	 h.Draw("same" if same else "")
#         same = True 
#    
#from itertools import combinations
#pdfname = "Crossplots.pdf"
#
#canv = ROOT.TCanvas()
#canv.Print(pdfname+"[") 
#
#for v1,v2 in combinations(plotvars,2):
#	bkg.Draw(v1+":"+v2,lptCuts)
#	canv.Print(pdfname,"") 
#canv.Print(pdfname+"]","")
