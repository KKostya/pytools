import ROOT 

ROOT.gROOT.SetBatch()

sigFile = [ROOT.TFile("../HToZZTo2L2Q_M-125_8TeV_PATtuple_WithPU.root"),
           ROOT.TFile("../GluGluToHToZZTo2L2Q_M-125_7TeV_PAT_WithPU.root")]

sig = [s.Get("HZZNTuples/NTuples") for s in sigFile]

from RooFuncs import MakeInvm,Register

MakeInvm(sig[0],"Mmm",["Mu","Mu"],["[0]","[1]"])
MakeInvm(sig[0],"Mee",["Ele","Ele"],["[0]","[1]"])
MakeInvm(sig[0],"Mjj",["Jet","Jet"],["[0]","[1]"])

for i in range(0,5):
    Register(sig[0],"DRjb{0}1".format(i), "sqrt((GenBPhi[0]-JetPhi[{0}])^2+(GenBEta[0]-JetEta[{0}])^2)".format(i))
    Register(sig[0],"DRjb{0}2".format(i), "sqrt((GenBPhi[1]-JetPhi[{0}])^2+(GenBEta[1]-JetEta[{0}])^2)".format(i))

########################## Cuts #########################33
## Cuts on jets CSVs
#nobtag   = ROOT.TCut("JetCsv[0] < 0.679 && JetCsv[1] < 0.679")
#fstbtag  = ROOT.TCut("JetCsv[0] > 0.679 && JetCsv[1] < 0.679")
#sndbtag  = ROOT.TCut("JetCsv[0] < 0.679 && JetCsv[1] > 0.679")
#twobtag  = ROOT.TCut("JetCsv[0] > 0.679 && JetCsv[1] > 0.679")

## Muons ## 
mqCuts = ROOT.TCut("JetPt@.size()>=2 && MuPt@.size()>=2 && MuCharge[0]*MuCharge[1] <0" )
mptCuts  = ROOT.TCut("MuPt[0] > 17 && MuPt[1] > 8 && Mmm > 20 && Mmm < 60")+mqCuts

## Electrons ##
eqCuts = ROOT.TCut("ElePt@.size()>=2 && EleCharge[0]*EleCharge[1] <0" )
eptCuts  = ROOT.TCut("ElePt[0] > 17 && ElePt[1] > 8 && Mee > 20 &&  Mee < 60")+eqCuts

#from PerCutPlotter import PerCutPlotter
from itertools import product
#plotter = PerCutPlotter("CutHists.pdf")

#plotter.PaveText("Preselection on top of everything:", ["Two leptons, opposite charge", "20<Mll<06","PtL1>17,PtL2>8"] )
for txt,s,cs,lu in zip(["8 TeV ","7 TeV "],sig,[72.81,57.14],[20,5]):
    #plotter.PaveText("Matching jets, " + txt + ":",["DRjb<0.5"])
#    norm ={"cs":cs,"lumi":lu,"title":"Events@"+str(lu)+" fb^{-1}:"}
#    for k in range(0,5):
#        cuts = [ ( "Match b1 to j{0}, b2 to j{1}".format(i+1,j+1),
#                 mptCuts + ROOT.TCut("DRjb{0}1 < 0.5 && DRjb{1}2 < 0.5".format(i,j)), [] )
#                 for i,j in product(range(0,5),range(0,5)) ]
#	#plotter.Draw(s,"JetCsv[{0}]".format(k),(100,0,1),"CSV for jet{0}".format(k+1),cuts,norm)
	
    for i in range(0,5):
	for j in range(0,5):
            cut = ROOT.TCut("DRjb{0}1 < 0.5 && DRjb{1}2 < 0.5".format(i,j)) + mptCuts
	    print "%3.3g &" % (cs*lu*s.Draw("JetPt[0]",cut)/s.GetEntries()),
	print  ""
#plotter.Finish()
