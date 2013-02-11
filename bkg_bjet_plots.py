import ROOT 

ROOT.gROOT.SetBatch()

bkgFile= [
	ROOT.TFile("../DYJetsToLL_M-50_TuneZ2Star_8TeV_1M.root"),
	ROOT.TFile("../TT_8TeV_1M.root") ]

bkg   = [s.Get("HZZNTuples/NTuples") for s in bkgFile]

from RooFuncs import MakeInvm,Register
MakeInvm(bkg[0],"Mmm",["Mu","Mu"],["[0]","[1]"])
MakeInvm(bkg[0],"Mjj",["BJet","BJet"],["[0]","[1]"])
MakeInvm(bkg[0],"Mmmjj",["BJet","BJet","Mu","Mu"],["[0]","[1]","[0]","[1]"])

MakeInvm(bkg[0],"gMmm",["GenMu","GenMu"],["[0]","[1]"])
MakeInvm(bkg[0],"gMbb",["GenB","GenB"],["[0]","[1]"])

Register(bkg[0],"DRjm11" , "sqrt((MuPhi[0]-BJetPhi[0])^2+(MuEta[0]-BJetEta[0])^2)")
Register(bkg[0],"DRjm12" , "sqrt((MuPhi[0]-BJetPhi[1])^2+(MuEta[0]-BJetEta[1])^2)")
Register(bkg[0],"DRjm21" , "sqrt((MuPhi[1]-BJetPhi[0])^2+(MuEta[1]-BJetEta[0])^2)")
Register(bkg[0],"DRjm22" , "sqrt((MuPhi[1]-BJetPhi[1])^2+(MuEta[1]-BJetEta[1])^2)")
Register(bkg[0],"DRjmmin", "min(DRjm11,min(DRjm12,min(DRjm21,DRjm22)))")
Register(bkg[0],"DRjmmax", "max(DRjm11,max(DRjm12,max(DRjm21,DRjm22)))")
 

########################## Cuts #########################33

# Two electrons and two jets
quantitiyCuts = ROOT.TCut("MuPt@.size()>=2 && BJetPt@.size()>=2 && MuCharge[0]*MuCharge[1] <0 && Mmm < 80" )

# Cuts on the lepton pt
#lptCuts  = ROOT.TCut("((DRjb11<0.5 && DRjb22<0.5) || (DRjb12<0.5 && DRjb21<0.5))")+quantitiyCuts
#lptCuts  = ROOT.TCut("((DRjb11<0.5 && DRjb22<0.5) || (DRjb12<0.5 && DRjb21<0.5))")+quantitiyCuts

# Cuts on lepton pt 
nopt   = ROOT.TCut("MuPt[0] < 17 && MuPt[1] < 8")
fstpt  = ROOT.TCut("MuPt[0] > 17 && MuPt[1] < 8")
sndpt  = ROOT.TCut("MuPt[0] < 17 && MuPt[1] > 8")
twopt  = ROOT.TCut("MuPt[0] > 17 && MuPt[1] > 8")

########################## Cuts info and colors #########################33
cuts =        [( quantitiyCuts +  nopt, "Pt#mu1 < 17, Pt#mu2 < 8" , ROOT.kBlue),
               ( quantitiyCuts + fstpt, "Pt#mu1 > 17, Pt#mu2 < 8" , ROOT.kGreen),
               ( quantitiyCuts + sndpt, "Pt#mu1 < 17, Pt#mu2 > 8" , ROOT.kGreen+3),
               ( quantitiyCuts + twopt, "Pt#mu1 > 17, Pt#mu2 > 8" , ROOT.kRed)  ]



ptHistsData = [ 
        ("Pt of #mu1", (100,0,200), "MuPt[0]" ,[]),
        ("Pt of #mu2", (100,0,200), "MuPt[1]" ,[]),
        ("Pt of bj1",   (100,0,200), "BJetPt[0]",[]),
        ("Pt of bj2",   (100,0,200), "BJetPt[1]",[])]

csvHistsData = [ 
        ("CSV of bj1"   , (100,0,1), "BJetCsv[0]" ,[]),
        ("CSV of bj2"   , (100,0,1), "BJetCsv[1]" ,[])
        ]

metHistsData = [ ("MET"   , (100,0,300), "MetEt[0]" ,[]) ]

mHistsData = [ 
        ("M#mu#mu" , (100,0,150), "Mmm" ,[]),
        ("Mjj"     , (100,0,150), "Mjj" ,[]),
        ("Gen Mmm" , (100,0,150), "gMmm" ,[]),
        ("Gen Mbb" , (100,0,150), "gMbb" ,[]) ]

drHistsData = [ 
        ("DR #mu1-j1",(100,0,7), "DRjm11" ,[]),
        ("DR #mu1-j2",(100,0,7), "DRjm12" ,[]),
        ("max DR ",   (100,0,7), "DRjmmax",[]),
        ("DR #mu2-j1",(100,0,7), "DRjm21" ,[]),
        ("DR #mu2-j2",(100,0,7), "DRjm22" ,[]),
        ("min DR ",    (100,0,7),"DRjmmin",[])
 ]



from StackPlotter import StackPlotter

plotter = StackPlotter("BJetBkgHists.pdf")

plotter.PaveText("Backgruounds",["Selection:","2 CVSM b-jets","2#mu - opposite signs", "M#mu#mu < 80"]) 

for txt,s,cs,lu in zip(["DY 8 TeV ","TT 8 TeV"],bkg,[2972.03,243.00],[20,20]):
	plotter.Draw(s  ,txt + "PT."  , cuts,  ptHistsData, {"cs":cs,"lumi":lu,"title":"Events@"+str(lu)+" fb^{-1}:"})
	plotter.Draw(s  ,txt + "met"  , cuts, metHistsData, {"cs":cs,"lumi":lu,"title":"Events@"+str(lu)+" fb^{-1}:"})
	plotter.Draw(s  ,txt + "Csv." , cuts, csvHistsData, {"cs":cs,"lumi":lu,"title":"Events@"+str(lu)+" fb^{-1}:"})
	plotter.Draw(s  ,txt + "inv." , cuts,   mHistsData, {"cs":cs,"lumi":lu,"title":"Events@"+str(lu)+" fb^{-1}:"})
	plotter.Draw(s  ,txt + "DR."  , cuts,  drHistsData, {"cs":cs,"lumi":lu,"title":"Events@"+str(lu)+" fb^{-1}:"})
plotter.Finish()
