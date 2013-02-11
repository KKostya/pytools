import ROOT 

ROOT.gROOT.SetBatch()

sigFile = [ROOT.TFile("../HToZZTo2L2Q_M-125_8TeV_PATtuple_WithPU.root"),
           ROOT.TFile("../GluGluToHToZZTo2L2Q_M-125_7TeV_PAT_WithPU.root")]

sig = [s.Get("HZZNTuples/NTuples") for s in sigFile]

from RooFuncs import MakeInvm,Register

MakeInvm(sig[0],"Mmm",["Mu","Mu"],["[0]","[1]"])
MakeInvm(sig[0],"Mee",["Ele","Ele"],["[0]","[1]"])
MakeInvm(sig[0],"Mjj",["BJet","BJet"],["[0]","[1]"])

for i in range(0,2):
    Register(sig[0],"DRjb{0}1".format(i), "sqrt((GenBPhi[0]-BJetPhi[{0}])^2+(GenBEta[0]-BJetEta[{0}])^2)".format(i))
    Register(sig[0],"DRjb{0}2".format(i), "sqrt((GenBPhi[1]-BJetPhi[{0}])^2+(GenBEta[1]-BJetEta[{0}])^2)".format(i))

## Muons ## 
mqCuts = ROOT.TCut("BJetPt@.size()>=2 && MuPt@.size()>=2 && MuCharge[0]*MuCharge[1] <0" )
mptCuts  = ROOT.TCut("MuPt[0] > 17 && MuPt[1] > 8 && Mmm < 60")+mqCuts

## Electrons ##
eqCuts = ROOT.TCut("ElePt@.size()>=2 && EleCharge[0]*EleCharge[1] <0" )
eptCuts  = ROOT.TCut("ElePt[0] > 17 && ElePt[1] > 8 &&  Mee < 60")+eqCuts

from itertools import product

for txt,s,cs,lu in zip(["8 TeV ","7 TeV "],sig,[72.81,57.14],[20,5]):
    for i in range(0,2):
	for j in range(0,2):
            cut = ROOT.TCut("DRjb{0}1 < 0.5 && DRjb{1}2 < 0.5".format(i,j)) + mptCuts
	    print "%3.3g &" % (cs*lu*s.Draw("BJetPt[0]",cut)/s.GetEntries()),
	print  ""
    for i in range(0,2):
	for j in range(0,2):
            cut = ROOT.TCut("DRjb{0}1 < 0.5 && DRjb{1}2 < 0.5".format(i,j)) + eptCuts
	    print "%3.3g &" % (cs*lu*s.Draw("BJetPt[0]",cut)/s.GetEntries()),
	print  ""

