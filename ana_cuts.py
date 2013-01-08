import ROOT 

ROOT.gROOT.SetBatch()

sigFile = [ROOT.TFile("../HToZZTo2L2Q_M-125_8TeV_PATtuple_WithPU.root"),
           ROOT.TFile("../GluGluToHToZZTo2L2Q_M-125_7TeV_PAT_WithPU.root")]

sig = [s.Get("HZZNTuples/NTuples") for s in sigFile]

from RooFuncs import MakeInvm,Register
MakeInvm(sig[0],"Mmm",["Mu","Mu"],["[0]","[1]"])
MakeInvm(sig[0],"Mee",["Ele","Ele"],["[0]","[1]"])
MakeInvm(sig[0],"Mjj",["Jet","Jet"],["[0]","[1]"])
MakeInvm(sig[0],"Mmmjj",["Jet","Jet","Mu","Mu"],["[0]","[1]","[0]","[1]"])
MakeInvm(sig[0],"Meejj",["Jet","Jet","Ele","Ele"],["[0]","[1]","[0]","[1]"])

MakeInvm(sig[0],"gMmm",["GenMu","GenMu"],["[0]","[1]"])
MakeInvm(sig[0],"gMee",["GenE","GenE"],["[0]","[1]"])
MakeInvm(sig[0],"gMbb",["GenB","GenB"],["[0]","[1]"])

Register(sig[0],"DRjb11" , "sqrt((GenBPhi[0]-JetPhi[0])^2+(GenBEta[0]-JetEta[0])^2)")
Register(sig[0],"DRjb12" , "sqrt((GenBPhi[0]-JetPhi[1])^2+(GenBEta[0]-JetEta[1])^2)")
Register(sig[0],"DRjb21" , "sqrt((GenBPhi[1]-JetPhi[0])^2+(GenBEta[1]-JetEta[0])^2)")
Register(sig[0],"DRjb22" , "sqrt((GenBPhi[1]-JetPhi[1])^2+(GenBEta[1]-JetEta[1])^2)")
Register(sig[0],"DRjbmin", "min(DRjb11,min(DRjb12,min(DRjb21,DRjb22)))")
 
Register(sig[0],"DRjm11" , "sqrt((MuPhi[0]-JetPhi[0])^2+(MuEta[0]-JetEta[0])^2)")
Register(sig[0],"DRjm12" , "sqrt((MuPhi[0]-JetPhi[1])^2+(MuEta[0]-JetEta[1])^2)")
Register(sig[0],"DRjm21" , "sqrt((MuPhi[1]-JetPhi[0])^2+(MuEta[1]-JetEta[0])^2)")
Register(sig[0],"DRjm22" , "sqrt((MuPhi[1]-JetPhi[1])^2+(MuEta[1]-JetEta[1])^2)")
Register(sig[0],"DRjmmin", "min(DRjm11,min(DRjm12,min(DRjm21,DRjm22)))")
 
Register(sig[0],"DRje11" , "sqrt((ElePhi[0]-JetPhi[0])^2+(EleEta[0]-JetEta[0])^2)")
Register(sig[0],"DRje12" , "sqrt((ElePhi[0]-JetPhi[1])^2+(EleEta[0]-JetEta[1])^2)")
Register(sig[0],"DRje21" , "sqrt((ElePhi[1]-JetPhi[0])^2+(EleEta[1]-JetEta[0])^2)")
Register(sig[0],"DRje22" , "sqrt((ElePhi[1]-JetPhi[1])^2+(EleEta[1]-JetEta[1])^2)")
Register(sig[0],"DRjemin", "min(DRje11,min(DRje12,min(DRje21,DRje22)))")

########################## Cuts #########################33
# Cuts on jets CSVs
nobtag   = ROOT.TCut("JetCsv[0] < 0.679 && JetCsv[1] < 0.679")
fstbtag  = ROOT.TCut("JetCsv[0] > 0.679 && JetCsv[1] < 0.679")
sndbtag  = ROOT.TCut("JetCsv[0] < 0.679 && JetCsv[1] > 0.679")
twobtag  = ROOT.TCut("JetCsv[0] > 0.679 && JetCsv[1] > 0.679")

## Muons ## 
mqCuts = ROOT.TCut("MuPt@.size()>=2 && JetPt@.size()>=2 && MuCharge[0]*MuCharge[1] <0" )
mptCuts  = ROOT.TCut("MuPt[0] > 17 && MuPt[1] > 8 && Mmm > 20 && Mmm < 60")+mqCuts
cutsM =       [( mptCuts + nobtag , "No btags"                 , ROOT.kBlue),
               ( mptCuts + fstbtag, "Only first b-tagged"      , ROOT.kGreen),
               ( mptCuts + sndbtag, "Only second b-tagged"     , ROOT.kGreen+3),
               ( mptCuts + twobtag, "Both b-tagged"            , ROOT.kRed)  ]

## Electrons ##
eqCuts = ROOT.TCut("ElePt@.size()>=2 && JetPt@.size()>=2 && EleCharge[0]*EleCharge[1] <0" )
eptCuts  = ROOT.TCut("ElePt[0] > 17 && ElePt[1] > 8 && Mee > 20 &&  Mee < 60")+eqCuts
cutsE =       [( eptCuts + nobtag , "No btags"                 , ROOT.kBlue),
               ( eptCuts + fstbtag, "Only first b-tagged"      , ROOT.kGreen),
               ( eptCuts + sndbtag, "Only second b-tagged"     , ROOT.kGreen+3),
               ( eptCuts + twobtag, "Both b-tagged"            , ROOT.kRed)  ]

############################ Histogramming #########################
csvHistsData = [ 
        ("CSV of j1"   , (100,0,1), "JetCsv[0]" ,[]),
        ("CSV of j2"   , (100,0,1), "JetCsv[1]" ,[]) ]

gdrHistsData = [ 
        ("DR genB1-j1",(100,0,7), "DRjb11" ,[]),
        ("DR genB1-j2",(100,0,7), "DRjb12" ,[]),
        ("DR genB2-j1",(100,0,7), "DRjb21" ,[]),
        ("DR genB2-j2",(100,0,7), "DRjb22" ,[]) ]

## Muons
mptHistsData = [ 
        ("Pt of #mu1", (100,0,200), "MuPt[0]" ,[]),
        ("Pt of #mu2", (100,0,200), "MuPt[1]" ,[]),
        ("Pt of j1",   (100,0,200), "JetPt[0]",[]),
        ("Pt of j2",   (100,0,200), "JetPt[1]",[])]

metHistsData = [ 
        ("Eta of #mu1", (100,-4,4), "MuEta[0]" ,[]),
        ("Eta of #mu2", (100,-4,4), "MuEta[1]" ,[]),
        ("Eta of j1",   (100,-4,4), "JetEta[0]",[]),
        ("Eta of j2",   (100,-4,4), "JetEta[1]",[])]

mHistsData = [ 
        ("M#mu#mu"  , (100,0,150), "Mmm"  ,[]),
        ("Mjj"      , (100,0,150), "Mjj"  ,[]),
        ("M#mu#mujj", (100,0,250), "Mmmjj",[]),
        ("Gen Mmm"  , (100,0,150), "gMmm" ,[]),
        ("Gen Mbb"  , (100,0,150), "gMbb" ,[]) ]

mdrHistsData = [ 
        ("DR #mu1-j1",(100,0,7), "DRjm11" ,[]),
        ("DR #mu1-j2",(100,0,7), "DRjm12" ,[]),
        ("DR #mu2-j1",(100,0,7), "DRjm21" ,[]),
        ("DR #mu2-j2",(100,0,7), "DRjm22" ,[]) ]

## Electrons

eptHistsData = [ 
        ("Pt of e1",   (100,0,200), "ElePt[0]" ,[]),
        ("Pt of e2",   (100,0,200), "ElePt[1]" ,[]),
        ("Pt of j1",   (100,0,200), "JetPt[0]",[]),
        ("Pt of j2",   (100,0,200), "JetPt[1]",[])]

eetHistsData = [ 
        ("Eta of e1",   (100,-4,4), "EleEta[0]" ,[]),
        ("Eta of e2",   (100,-4,4), "EleEta[1]" ,[]),
        ("Eta of j1",   (100,-4,4), "JetEta[0]",[]),
        ("Eta of j2",   (100,-4,4), "JetEta[1]",[])]

eHistsData = [ 
        ("Mee"     , (100,0,150), "Mee" ,[]),
        ("Mjj"     , (100,0,150), "Mjj" ,[]),
        ("Meejj"   , (100,0,250), "Meejj",[]),
        ("Gen Mmm" , (100,0,150), "gMee" ,[]),
        ("Gen Mbb" , (100,0,150), "gMbb" ,[]) ]

edrHistsData = [ 
        ("DR e1-j1",(100,0,7), "DRje11" ,[]),
        ("DR e1-j2",(100,0,7), "DRje12" ,[]),
        ("DR e2-j1",(100,0,7), "DRje21" ,[]),
        ("DR e2-j2",(100,0,7), "DRje22" ,[]) ]

from StackPlotter import StackPlotter

plotter = StackPlotter("CutHists.pdf")
for txt,s,cs,lu in zip(["8 TeV ","7 TeV "],sig,[72.81,57.14],[20,5]):
	plotter.PaveText("Analyzing cuts, muons",["Selection:","2jets,2#mu - opposite signs","MuPt > 17,8"]) 
	plotter.Draw(s ,txt + "PT"       , cutsM, mptHistsData, {"cs":cs,"lumi":lu,"title":"Events@"+str(lu)+" fb^{-1}:"})
	plotter.Draw(s ,txt + "Eta"      , cutsM, metHistsData, {"cs":cs,"lumi":lu,"title":"Events@"+str(lu)+" fb^{-1}:"})
	plotter.Draw(s ,txt + "Csv"      , cutsM, csvHistsData, {"cs":cs,"lumi":lu,"title":"Events@"+str(lu)+" fb^{-1}:"})
	plotter.Draw(s ,txt + "inv mass" , cutsM,   mHistsData, {"cs":cs,"lumi":lu,"title":"Events@"+str(lu)+" fb^{-1}:"})
	plotter.Draw(s ,txt + "#mu-j DR" , cutsM, mdrHistsData, {"cs":cs,"lumi":lu,"title":"Events@"+str(lu)+" fb^{-1}:"})
	plotter.Draw(s ,txt + "genb-j DR", cutsM, gdrHistsData, {"cs":cs,"lumi":lu,"title":"Events@"+str(lu)+" fb^{-1}:"})
	plotter.PaveText("Analyzing cuts, electrons",["Selection:","2jets,2e - opposite signs","ElePt>17,8"]) 
	plotter.Draw(s ,txt + "PT"       , cutsE, eptHistsData, {"cs":cs,"lumi":lu,"title":"Events@"+str(lu)+" fb^{-1}:"})
	plotter.Draw(s ,txt + "Eta"      , cutsE, eetHistsData, {"cs":cs,"lumi":lu,"title":"Events@"+str(lu)+" fb^{-1}:"})
	plotter.Draw(s ,txt + "Csv"      , cutsE, csvHistsData, {"cs":cs,"lumi":lu,"title":"Events@"+str(lu)+" fb^{-1}:"})
	plotter.Draw(s ,txt + "inv mass" , cutsE,   eHistsData, {"cs":cs,"lumi":lu,"title":"Events@"+str(lu)+" fb^{-1}:"})
	plotter.Draw(s ,txt + "e-j DR"   , cutsE, edrHistsData, {"cs":cs,"lumi":lu,"title":"Events@"+str(lu)+" fb^{-1}:"})
	plotter.Draw(s ,txt + "genb-j DR", cutsE, gdrHistsData, {"cs":cs,"lumi":lu,"title":"Events@"+str(lu)+" fb^{-1}:"})
plotter.Finish()
