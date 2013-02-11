import ROOT
import re

ntuplename = "HZZNTuples/NTuples"
hltname = "HZZNTuples/HLTNames"

nts = [   
            ("Signal",     72. , "HToZZTo2L2Q_M-125_8TeV_PATtuple_1M.root"    , ROOT.kRed),
            ("DY",    2972030. , "DYJetsToLL_M-50_TuneZ2Star_8TeV_1M.root"    , ROOT.kGreen),
            ("DY1",    549000. , "DY1JetsToLL_M-50_TuneZ2Star_8TeV_1M.root"   , ROOT.kGreen),
            ("DY2",    181990. , "DY2JetsToLL_M-50_TuneZ2Star_8TeV_1M.root"   , ROOT.kGreen),
            ("DY4",     23004  , "DY4JetsToLL_M-50_TuneZ2Star_8TeV_1M.root"   , ROOT.kGreen),
            ("DYM",  11271240. , "DYJetsToLL_M-10To50filter_8TeV_1M.root"     , ROOT.kGreen),
            ("TT2l2n2b",17901. , "TTTo2L2Nu2B_8TeV_1M.root"                   , ROOT.kBlack),
            ("TTLept",      1. , "TTJets_FullLeptMGDecays_8TeV_1M.root"       , ROOT.kBlack),
            ("TTHadr",      1. , "TTJets_HadronicMGDecays_8TeV_1M.root"       , ROOT.kBlack),
            ("TT",          1. , "TT_8TeV_1M.root"                            , ROOT.kBlack),
            ("TbTW",        1. , "Tbar_tW-channel-DR_TuneZ2star_8TeV_1M.root" , ROOT.kBlack),
            ("WW",          1. , "WW_TuneZ2star_8TeV_1M.root"                 , ROOT.kGray),
            ("ZZ2l2q",    784. , "ZZJetsTo2L2Q_TuneZ2star_8TeV_1M.root"       , ROOT.kGray),
            ("ZZ",          1. , "ZZ_TuneZ2star_8TeV_1M.root"                 , ROOT.kGray)
           ]

#################################  
class DataManager:
    def __init__(self,dir):
      self.files  = {}
      self.fnames  = {}
      self.eqlumis  = {}
      self.colors = {}
      for n,cs,f,c in nts:
          self.fnames[n] = dir+"/"+f
          self.files[n] = ROOT.TFile(self.fnames[n])
          self.eqlumis[n] = self.Tree(n).GetEntries()/cs
          self.colors[n] = c

    def  Tree(self,n): return self.files[n].Get(ntuplename)
    def  HLTs(self,n): return self.files[n].Get(hltname)
    def  Lumi(self,n): return self.eqlumis[n]
    def Color(self,n): return self.colors[n]

    def Names(self): return [n for n,a,b,c in nts]
    def RgxNames(self,rgx): 
        r = re.compile(rgx)
        return [n for n in self.files if r.match(n) != None]

