import ROOT 

def SumP4(prfxs,pofxs):
    strs = ["{0}Energy{1}","{0}Pt{1}*cos({0}Phi{1})","{0}Pt{1}*sin({0}Phi{1})","{0}Pt{1}*sinh({0}Eta{1})"]
    return ["+".join(s.format(a,b) for a,b in zip(prfxs,pofxs)) for s in strs]
        

def MakeInvm(tree,name,prfxs,pofxs):
        fstring = "sqrt(({0})^2-({1})^2-({2})^2-({3})^2)".format(*SumP4(prfxs,pofxs))
        tf = ROOT.TTreeFormula(name,fstring,tree)
        ROOT.gROOT.GetListOfFunctions().Add(tf)

def Register(tree,name,func):
    tf = ROOT.TTreeFormula(name,func,tree)
    ROOT.gROOT.GetListOfFunctions().Add(tf)
