import ROOT 

ROOT.gROOT.SetBatch()

sigFile   = [ROOT.TFile("../HToZZTo2L2Q_M-125_8TeV_PATtuple_WithoutPU.root"),
             ROOT.TFile("../GluGluToHToZZTo2L2Q_M-125_7TeV_PAT_WithoutPU.root")]

sigFilePU = [ROOT.TFile("../HToZZTo2L2Q_M-125_8TeV_PATtuple_WithPU.root"),
	     ROOT.TFile("../GluGluToHToZZTo2L2Q_M-125_7TeV_PAT_WithPU.root")]

sig   = [s.Get("HZZNTuples/NTuples") for s in sigFile]
sigPU = [s.Get("HZZNTuples/NTuples") for s in sigFilePU]

from RooFuncs import MakeInvm,Register
MakeInvm(sig[0],"Mmm",["Mu","Mu"],["[0]","[1]"])
MakeInvm(sig[0],"Mjj",["Jet","Jet"],["[0]","[1]"])
MakeInvm(sig[0],"Mmmjj",["Jet","Jet","Mu","Mu"],["[0]","[1]","[0]","[1]"])

MakeInvm(sig[0],"gMmm",["GenMu","GenMu"],["[0]","[1]"])
MakeInvm(sig[0],"gMbb",["GenB","GenB"],["[0]","[1]"])

Register(sig[0],"DRjb11" , "sqrt((GenBPhi[0]-JetPhi[0])^2+(GenBEta[0]-JetEta[0])^2)")
Register(sig[0],"DRjb12" , "sqrt((GenBPhi[0]-JetPhi[1])^2+(GenBEta[0]-JetEta[1])^2)")
Register(sig[0],"DRjb21" , "sqrt((GenBPhi[1]-JetPhi[0])^2+(GenBEta[1]-JetEta[0])^2)")
Register(sig[0],"DRjb22" , "sqrt((GenBPhi[1]-JetPhi[1])^2+(GenBEta[1]-JetEta[1])^2)")
Register(sig[0],"DRjbmin", "min(DRjb11,min(DRjb12,min(DRjb21,DRjb22)))")
 

########################## Cuts #########################33

# Two electrons and two jets
quantitiyCuts = ROOT.TCut("MuPt@.size()>=2 && JetPt@.size()>=2 && MuCharge[0]*MuCharge[1] <0" )

# Cuts on the lepton pt
lptCuts  = ROOT.TCut("((DRjb11<0.5 && DRjb22<0.5) || (DRjb12<0.5 && DRjb21<0.5))")+quantitiyCuts

# Cuts on jets CSVs
nobtag   = ROOT.TCut("JetCsv[0] < 0.679 && JetCsv[1] < 0.679")
fstbtag  = ROOT.TCut("JetCsv[0] > 0.679 && JetCsv[1] < 0.679")
sndbtag  = ROOT.TCut("JetCsv[0] < 0.679 && JetCsv[1] > 0.679")
twobtag  = ROOT.TCut("JetCsv[0] > 0.679 && JetCsv[1] > 0.679")

########################## Cuts info and colors #########################33
cuts =        [( lptCuts + nobtag , "No btags"                 , ROOT.kBlue),
               ( lptCuts + fstbtag, "Only first b-tagged"      , ROOT.kGreen),
               ( lptCuts + sndbtag, "Only second b-tagged"     , ROOT.kGreen+3),
               ( lptCuts + twobtag, "Both b-tagged"            , ROOT.kRed)  ]



ptHistsData = [ 
        ("Pt of #mu1", (100,0,200), "MuPt[0]" ,[]),
        ("Pt of #mu2", (100,0,200), "MuPt[1]" ,[]),
        ("Pt of j1",   (100,0,200), "JetPt[0]",[]),
        ("Pt of j2",   (100,0,200), "JetPt[1]",[])]

csvHistsData = [ 
        ("CSV of j1"   , (100,0,1), "JetCsv[0]" ,[]),
        ("CSV of j2"   , (100,0,1), "JetCsv[1]" ,[])
        ]

mHistsData = [ 
        ("M#mu#mu" , (100,0,150), "Mmm" ,[]),
        ("Mjj"     , (100,0,150), "Mjj" ,[]),
        ("Gen Mmm" , (100,0,150), "gMmm" ,[]),
        ("Gen Mbb" , (100,0,150), "gMbb" ,[]) ]

drHistsData = [ 
        ("DR genB1-j1",(100,0,7), "DRjb11" ,[]),
        ("DR genB1-j2",(100,0,7), "DRjb12" ,[]),
        ("DR genB2-j1",(100,0,7), "DRjb21" ,[]),
        ("DR genB2-j2",(100,0,7), "DRjb22" ,[]) ]



from StackPlotter import StackPlotter

plotter = StackPlotter("Hists.pdf")

plotter.PaveText("Mjj and PU",["Selection:","2jets,2#mu - opposite signs","DR(j1,genb1),DR(j2,genb2)<0.5 or DR(j1,genb2),DR(j2,genb1)<0.5 "]) 

for txt,s,spu in [("8 TeV ",sig[0],sigPU[0]),("7 TeV ",sig[1],sigPU[1])]:
	plotter.Draw(s  ,txt + "PT without PU."  , cuts,  ptHistsData)
	plotter.Draw(spu,txt + "PT with PU."  , cuts,  ptHistsData)
	plotter.Draw(s  ,txt + "Csv without PU." , cuts, csvHistsData)
	plotter.Draw(spu,txt + "Csv with PU." , cuts, csvHistsData)
	plotter.Draw(s  ,txt + "inv mass without PU." , cuts, mHistsData)
	plotter.Draw(spu,txt + "inv mass with PU." , cuts, mHistsData)
	plotter.Draw(s  ,txt + "DR without PU." , cuts, drHistsData)
	plotter.Draw(spu,txt + "DR with PU." , cuts, drHistsData)
plotter.Finish()
