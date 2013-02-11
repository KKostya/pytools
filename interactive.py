import ROOT 

import RootTools.DataManager

dm = RootTools.DataManager.DataManager("..")
sig = dm.Tree("Signal")

from RootTools.RooFuncs import MakeInvm,Register

MakeInvm(sig,"Mmm",  ["Mu","Mu"],["[0]","[1]"])
MakeInvm(sig,"Mee",  ["Ele","Ele"],["[0]","[1]"])
MakeInvm(sig,"Mjj",  ["Jet","Jet"],["[0]","[1]"])
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

from RootTools import CutsCollection
