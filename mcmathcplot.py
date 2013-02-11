import ROOT
from RooFuncs import MakeInvm,Register
import DataManager

dm = DataManager.DataManager("..")
sig = dm.Tree("Signal")

MakeInvm(sig,"Mmm",["Mu","Mu"],["[0]","[1]"])
MakeInvm(sig,"Mee",["Ele","Ele"],["[0]","[1]"])
MakeInvm(sig,"Mjj",["Jet","Jet"],["[0]","[1]"])
MakeInvm(sig,"Mmmjj",["Jet","Jet","Mu","Mu"],["[0]","[1]","[0]","[1]"])
MakeInvm(sig,"Meejj",["Jet","Jet","Ele","Ele"],["[0]","[1]","[0]","[1]"])

MakeInvm(sig,"gMmm",["GenMu","GenMu"],["[0]","[1]"])
MakeInvm(sig,"gMee",["GenE","GenE"],["[0]","[1]"])
MakeInvm(sig,"gMbb",["GenB","GenB"],["[0]","[1]"])

Register(sig,"DRjb11" , "sqrt((GenBPhi[0]-JetPhi[0])^2+(GenBEta[0]-JetEta[0])^2)")
Register(sig,"DRjb12" , "sqrt((GenBPhi[0]-JetPhi[1])^2+(GenBEta[0]-JetEta[1])^2)")
Register(sig,"DRjb21" , "sqrt((GenBPhi[1]-JetPhi[0])^2+(GenBEta[1]-JetEta[0])^2)")
Register(sig,"DRjb22" , "sqrt((GenBPhi[1]-JetPhi[1])^2+(GenBEta[1]-JetEta[1])^2)")
Register(sig,"DRjbmin", "min(DRjb11,min(DRjb12,min(DRjb21,DRjb22)))")

Register(sig,"DRjm11" , "sqrt((MuPhi[0]-JetPhi[0])^2+(MuEta[0]-JetEta[0])^2)")
Register(sig,"DRjm12" , "sqrt((MuPhi[0]-JetPhi[1])^2+(MuEta[0]-JetEta[1])^2)")
Register(sig,"DRjm21" , "sqrt((MuPhi[1]-JetPhi[0])^2+(MuEta[1]-JetEta[0])^2)")
Register(sig,"DRjm22" , "sqrt((MuPhi[1]-JetPhi[1])^2+(MuEta[1]-JetEta[1])^2)")
Register(sig,"DRjmmin", "min(DRjm11,min(DRjm12,min(DRjm21,DRjm22)))")

Register(sig,"DRje11" , "sqrt((ElePhi[0]-JetPhi[0])^2+(EleEta[0]-JetEta[0])^2)")
Register(sig,"DRje12" , "sqrt((ElePhi[0]-JetPhi[1])^2+(EleEta[0]-JetEta[1])^2)")
Register(sig,"DRje21" , "sqrt((ElePhi[1]-JetPhi[0])^2+(EleEta[1]-JetEta[0])^2)")
Register(sig,"DRje22" , "sqrt((ElePhi[1]-JetPhi[1])^2+(EleEta[1]-JetEta[1])^2)")
Register(sig,"DRjemin", "min(DRje11,min(DRje12,min(DRje21,DRje22)))")

########################## Cuts #########################33
# Cuts on jets CSVs
nobtag   = ROOT.TCut("JetCsv[0] < 0.679 && JetCsv[1] < 0.679")
fstbtag  = ROOT.TCut("JetCsv[0] > 0.679 && JetCsv[1] < 0.679")
sndbtag  = ROOT.TCut("JetCsv[0] < 0.679 && JetCsv[1] > 0.679")
twobtag  = ROOT.TCut("JetCsv[0] > 0.679 && JetCsv[1] > 0.679")

## Muons ## 
mqCuts = ROOT.TCut("MuPt@.size()>=2 && JetPt@.size()>=2 && MuCharge[0]*MuCharge[1] <0 && MuGood[0]==1 && MuGood[1]==1 && JetGood[0]==1 && JetGood[1]==1" )
cuts  = mqCuts+ROOT.TCut("(DRjb11<0.5 && DRjb22<0.5)||(DRjb12<0.5 && DRjb21<0.5)")
cutsM =       [( cuts + nobtag , "No btags"                 , ROOT.kBlue),
               ( cuts + fstbtag, "Only first b-tagged"      , ROOT.kGreen),
               ( cuts + sndbtag, "Only second b-tagged"     , ROOT.kGreen+3),
               ( cuts + twobtag, "Both b-tagged"            , ROOT.kRed)  ]

   
mHistsData = [ ("M#mu#mu"  , (100,0,100), "Mmm"  ,[])]

from StackPlotter import StackPlotter
plotter = StackPlotter("MC_Match.pdf")
plotter.Draw(dm.Tree("Signal"),"Matching jets to GEN b-quarks", cutsM, mHistsData, {"cs":72.,"lumi":20,"title":"Events@20 fb^{-1}:"})
plotter.Finish()
