import ROOT
import array 

sigFile= ROOT.TFile("../HToZZTo2L2Q_M-125_8TeV_PATtuple_WithPU.root")
sig = sigFile.Get("HZZNTuples/NTuples")

bkg = ROOT.TChain("HZZNTuples/NTuples")
bkg.Add("../DYJetsToLL_M-50_TuneZ2Star_8TeV_1M.root")
bkg.Add("../DY1JetsToLL_M-50_TuneZ2Star_8TeV_1M.root")
bkg.Add("../DY2JetsToLL_M-50_TuneZ2Star_8TeV_1M.root")

################################ Cuts and prefiltering #############################################################

# Two muons 
quantitiyCuts = ROOT.TCut("MuPt@.size()>=2 && MuCharge[0]*MuCharge[1] <0" )
# Btags
tagCuts = ROOT.TCut("(JetCsv[0]>0.679?1:0)+(JetCsv[1]>0.679?1:0)+(JetCsv[2]>0.679?1:0)+(JetCsv[3]>0.679?1:0) >=2")+quantitiyCuts
# Cut in transverse momenta
lptCuts  = ROOT.TCut("MuPt[0] > 10")+tagCuts

# 2DO -- check existing file
tempf = ROOT.TFile("temp.root","recreate")
print  "Prefilter signal ..."
sigF  = sig.CopyTree(lptCuts.GetTitle())
print " ... done"
print  "Prefilter background ..."
bkgF  = bkg.CopyTree(lptCuts.GetTitle())
print " ... done"


#############################################################################################
from RooFuncs import MakeInvm,Register,SumP4

allvars = ["MetEt[0]","MuPt[0]","MuPt[1]","BJetPt[0]","BJetPt[1]","BJetCsv[0]","BJetCsv[1]"]

for nm,f in [
	("DR","sqrt((MuPhi[{0}]-BJetPhi[{1}])^2+(MuEta[{0}]-BJetEta[{1}])^2)"),
	("DE","sqrt((MuPhi[{0}]-BJetPhi[{1}])^2+(MuEta[{0}]-BJetEta[{1}])^2)"),
	("DP","sqrt((MuPhi[{0}]-BJetPhi[{1}])^2+(MuEta[{0}]-BJetEta[{1}])^2)") ]:
	
	Register(bkg,nm + "jm11" , f.format(0,0))
	Register(bkg,nm + "jm12" , f.format(0,1))
	Register(bkg,nm + "jm21" , f.format(1,0))
	Register(bkg,nm + "jm22" , f.format(1,1))

	allvars += [ nm + "jm11", nm + "jm12", nm + "jm21", nm + "jm22"]
	
#############################################################################################

####
###  This is a class that uses formula-defined variables and
###  submits them to MVA-reader using arrays
####
class MvaVars:
    ###
    ### Constructor requires a tree (which you can change later), an TMVA.Reader object
    ### and a list of variable names or expressions, which will be used in TTreeFormula evaluation
    ###
    def __init__(self,vars,reader,tree):
        self.arrays = {}
        self.formulae = {}
        self.tree = tree
        for v in vars: 
            self.arrays[v] = array.array('f',[0])
            reader.AddVariable(v,self.arrays[v])
            self.formulae[v] = ROOT.TTreeFormula(v,v,self.tree)

    def SetTree(self,tree): 
        self.tree = tree
        for v in self.formulae: 
            self.formulae[v] = ROOT.TTreeFormula(v,v,self.tree)

    ###
    ### This is analogous to the TTree.GetEntry method -- it evaluates all the formula
    ### and put results in correspondin arrays in memory
    ###
    def GetEntry(self,nentry):
        self.tree.GetEntry(nentry)
        for v in self.arrays:
            self.arrays[v][0] = self.formulae[v].EvalInstance()

reader = ROOT.TMVA.Reader()
vars = MvaVars(allvars,reader,sigF)
reader.BookMVA("BDT","weights/TMVAClassification_BDT.weights.xml")

print "Sig responses:"
hs = ROOT.TH1F("sig","sig",100,-1,1)
for i in range(1,sigF.GetEntries()-1):
	vars.GetEntry(i)
        hs.Fill(reader.EvaluateMVA("BDT"))

hs.Scale(20.*72./sig.GetEntries())

bs = ROOT.TH1F("bkg","bkg",100,-1,1)
print "Bkg responses:"
vars.SetTree(bkgF)
for i in range(1,bkgF.GetEntries()-1):
	vars.GetEntry(i)
	bs.Fill(reader.EvaluateMVA("BDT"))

bs.Scale(20.*(2972030.+549000.+181990.)/sig.GetEntries())

hs.Draw()
bs.Draw("same")
