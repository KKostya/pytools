import ROOT
import array
from RooFuncs import MakeInvm,Register,SumP4

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

class Bdt:
    def __init__(self,name,cuts,tree):
        self.name = name
        self.cuts = cuts
        self.vars = ["MetEt[0]","MuPt[0]","MuPt[1]","BJetPt[0]","BJetPt[1]","BJetCsv[0]","BJetCsv[1]"]
        for nm,f in [
            ("DR","sqrt((MuPhi[{0}]-BJetPhi[{1}])^2+(MuEta[{0}]-BJetEta[{1}])^2)"),
            ("DE","sqrt((MuPhi[{0}]-BJetPhi[{1}])^2+(MuEta[{0}]-BJetEta[{1}])^2)"),
            ("DP","sqrt((MuPhi[{0}]-BJetPhi[{1}])^2+(MuEta[{0}]-BJetEta[{1}])^2)") ]:
            Register(tree,nm + "jm11" , f.format(0,0))
            Register(tree,nm + "jm12" , f.format(0,1))
            Register(tree,nm + "jm21" , f.format(1,0))
            Register(tree,nm + "jm22" , f.format(1,1))
            self.vars += [ nm + "jm11", nm + "jm12", nm + "jm21", nm + "jm22"]
	
    def Train(self,sig,bkg,nsig,nbkg):
        fout = ROOT.TFile(self.name+"BDT.root","RECREATE")
        params = [ "!V", "!Silent", "Color", "DrawProgressBar", "Transformations=I;D;P;G,D", "AnalysisType=Classification"]
        factory = ROOT.TMVA.Factory(self.name, fout, ":".join(params))
        [factory.AddVariable(v,"F") for v in self.vars]

        factory.AddTree(sig,"Signal",1,self.cuts)
        factory.AddTree(bkg,"Background",1,self.cuts)

        params = [ "nTrain_Signal="+str(nsig), "nTrain_Background="+str(nbkg), "SplitMode=Random", "NormMode=NumEvents", "!V"]
        factory.PrepareTrainingAndTestTree(ROOT.TCut(""),":".join(params))

        params = [ "!H", "!V", "MaxDepth=10" ]
        factory.BookMethod(ROOT.TMVA.Types.kBDT, "BDT", ":".join(params))

        factory.TrainAllMethods()
        factory.TestAllMethods()
        factory.EvaluateAllMethods()

    def FillHist(self,hist,tree):
        tempf = ROOT.TFile("temp.root","recreate")
        treeF  = tree.CopyTree(self.cuts.GetTitle())

        reader = ROOT.TMVA.Reader()
        vars = MvaVars(self.vars,reader,treeF)
        reader.BookMVA("BDT","weights/"+self.name+"_BDT.weights.xml")

        for i in range(1,treeF.GetEntries()-1):
            vars.GetEntry(i)
            hist.Fill(reader.EvaluateMVA("BDT"))




