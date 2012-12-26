import ROOT 

ROOT.gROOT.SetBatch()

dyFile = ROOT.TFile("../DYJetsToLL_M-50_TuneZ2Star_8TeV_WithPU.root")
ttFile = ROOT.TFile("../TT_8TeV_WithPU.root")

bkg   = [s.Get("HZZNTuples/NTuples") for s in [dyFile,ttFile]]

from RooFuncs import MakeInvm,Register
MakeInvm(bkg[0],"Mmm",["Mu","Mu"],["[0]","[1]"])
MakeInvm(bkg[0],"Mjj",["Jet","Jet"],["[0]","[1]"])
MakeInvm(bkg[0],"Mmmjj",["Jet","Jet","Mu","Mu"],["[0]","[1]","[0]","[1]"])

########################## Cuts #########################33

# Two electrons and two jets
quantitiyCuts = ROOT.TCut("MuPt@.size()>=2 && JetPt@.size()>=2 && MuCharge[0]*MuCharge[1] <0" )

lptCuts  = ROOT.TCut("Mmm<60 && MuPt[0] > 17 && MuPt[1] > 8")+quantitiyCuts

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
        ("Mmmjj" , (100,0,150), "gMmm" ,[]) ]

from StackPlotter import StackPlotter

plotter = StackPlotter("Hists.pdf")

plotter.PaveText("8 TeV Backgroinds",["Selection:","2jets,2#mu - opposite signs","PFNoPileUp is \'off\'"]) 

for txt,t in zip(["DY ","TT "],bkg):
	plotter.Draw(t,txt + "PT."  , cuts,  ptHistsData)
	plotter.Draw(t,txt + "Csv." , cuts, csvHistsData)
	plotter.Draw(t,txt + "inv mass." , cuts, mHistsData)
	plotter.Draw(t,txt + "DR." , cuts, drHistsData)
plotter.Finish()
