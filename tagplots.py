import ROOT 

sigFile   = ROOT.TFile("../HToZZTo2L2Q_M-125_8TeV_PATtuple_WithoutPU.root")
sigFilePU = ROOT.TFile("../HToZZTo2L2Q_M-125_8TeV_PATtuple_WithPU.root")

sig   = sigFile.Get("HZZNTuples/NTuples")
sigPU = sigFilePU.Get("HZZNTuples/NTuples")

from RooFuncs import MakeInvm,Register
MakeInvm(sig,"Mmm",["Mu","Mu"],["[0]","[1]"])
MakeInvm(sig,"Mjj",["Jet","Jet"],["[0]","[1]"])
MakeInvm(sig,"Mmmjj",["Jet","Jet","Mu","Mu"],["[0]","[1]","[0]","[1]"])

MakeInvm(sig,"gMmm",["GenMu","GenMu"],["[0]","[1]"])
MakeInvm(sig,"gMbb",["GenB","GenB"],["[0]","[1]"])

Register(sig,"DRjb11" , "sqrt((GenBPhi[0]-JetPhi[0])^2+(GenBEta[0]-JetEta[0])^2)")
Register(sig,"DRjb12" , "sqrt((GenBPhi[0]-JetPhi[1])^2+(GenBEta[0]-JetEta[1])^2)")
Register(sig,"DRjb21" , "sqrt((GenBPhi[1]-JetPhi[0])^2+(GenBEta[1]-JetEta[0])^2)")
Register(sig,"DRjb22" , "sqrt((GenBPhi[1]-JetPhi[1])^2+(GenBEta[1]-JetEta[1])^2)")
Register(sig,"DRjbmin", "min(DRjb11,min(DRjb12,min(DRjb21,DRjb22)))")
 

########################## Cuts #########################33

# Two electrons and two jets
quantitiyCuts = ROOT.TCut("MuPt@.size()>=2 && JetPt@.size()>=2 && MuCharge[0]*MuCharge[1] <0" )

# Cuts on the lepton pt
lptCuts  = ROOT.TCut("gMmm<60 && DRjb11<0.5 && DRjb22<0.5")+quantitiyCuts

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

plotter.PaveText("Mjj and PU",["Selection:","2jets,2#mu - opposite signs","DR(j1,genb1),DR(j2,genb2)<0.5","M(gen#mu1,gen#mu2)<60"]) 

plotter.Draw(sig  ,"Btag cuts PT without PU."  , cuts,  ptHistsData)
plotter.Draw(sigPU,"Btag cuts PT with PU."  , cuts,  ptHistsData)
plotter.Draw(sig  ,"Btag cuts Csv without PU." , cuts, csvHistsData)
plotter.Draw(sigPU,"Btag cuts Csv with PU." , cuts, csvHistsData)
plotter.Draw(sig  ,"Btag cuts inv mass without PU." , cuts, mHistsData)
plotter.Draw(sigPU,"Btag cuts inv mass with PU." , cuts, mHistsData)
plotter.Draw(sig  ,"Btag cuts DR without PU." , cuts, drHistsData)
plotter.Draw(sigPU,"Btag cuts DR with PU." , cuts, drHistsData)
plotter.Finish()
