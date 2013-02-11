import ROOT 

ROOT.gROOT.SetBatch()
############################### Input data #########################################

ntData = [  
            ("DY",    3503700. , "../DYJetsToLL_M-50_TuneZ2Star_8TeV_1M.root"    , ROOT.kGreen),
            ("DY1",    666000. , "../DY1JetsToLL_M-50_TuneZ2Star_8TeV_1M.root"   , ROOT.kGreen-3),
            ("DY2",    215000. , "../DY2JetsToLL_M-50_TuneZ2Star_8TeV_1M.root"   , ROOT.kGreen+3),
            ("TT",      23640. , "../TTTo2L2Nu2B_8TeV_1M.root"                  , ROOT.kBlack),
            ("ZZ",        784. , "../ZZJetsTo2L2Q_TuneZ2star_8TeV_1M.root"      , ROOT.kGray),
            ("Signal",   72.81 , "../HToZZTo2L2Q_M-125_8TeV_PATtuple_1M.root", ROOT.kRed)   ]
lumi = 20.


######################################################################################
gcDat = []
canv = ROOT.TCanvas("HZZ Plot")

files = [ROOT.TFile(c) for a,b,c,d in ntData] # <- files should be kept open or GC will bite you 

trees = [(a,b,c.Get("HZZNTuples/NTuples"),co) for (a,b,d,co),c in zip(ntData,files)]

from RooFuncs import MakeInvm,Register,SumP4
MakeInvm(trees[0][2],"Mmm",["Mu","Mu"],["[0]","[1]"])
MakeInvm(trees[0][2],"Mbb",["BJet","BJet"],["[0]","[1]"])
MakeInvm(trees[0][2],"Mmmbb",["BJet","BJet","Mu","Mu"],["[0]","[1]","[0]","[1]"])
MakeInvm(trees[0][2],"Mjj",["Jet","Jet"],["[0]","[1]"])
MakeInvm(trees[0][2],"Mmmjj",["Jet","Jet","Mu","Mu"],["[0]","[1]","[0]","[1]"])

Register(trees[0][2],"SumPxB" , SumP4(["Mu","Mu","BJet","BJet"],["[0]","[1]","[0]","[1]"])[1])
Register(trees[0][2],"SumPyB" , SumP4(["Mu","Mu","BJet","BJet"],["[0]","[1]","[0]","[1]"])[2])
Register(trees[0][2],"SumPtB" , "sqrt(SumPxB^2+SumPyB^2)")

Register(trees[0][2],"SumPx" , SumP4(["Mu","Mu","Jet","Jet"],["[0]","[1]","[0]","[1]"])[1])
Register(trees[0][2],"SumPy" , SumP4(["Mu","Mu","Jet","Jet"],["[0]","[1]","[0]","[1]"])[2])
Register(trees[0][2],"SumPt" , "sqrt(SumPx^2+SumPy^2)")


def evts(c):
    ret = []
    nums = [t.Draw("BJetPt@.size()",c) for a,b,t,co in trees]
    for (tit, cs, tree, co), num in zip(trees,nums):
	    ret.append((tit, cs * lumi * float(num)/tree.GetEntries(), num))
    return ret


from math import log10, floor
def roundsig(x):  return str(round(x, 3-int(floor(log10(x)))))


def printTable(cuta,cutb,namea,nameb):
	print "\\begin{table}[H]"
	print "\\begin{tabular}{|l"+"|c"*len(trees)+"|"+"|c"*len(trees)+"|}"
	print "\\hline"
	print "&"+"\\multicolumn{"+str(len(trees))+"}{|c|}{"+namea+"}&\\multicolumn{"+str(len(trees))+"}{|c|}{"+nameb+"}\\\\\\hline"
	print ("&"+ "&".join([x[0] for x in trees]))*2 + "\\\\\\hline"
	for n,m in [ ("No $p^\mu_t$ cut", ""),
		     ("$p^{\mu_1}_t>7$"  , "MuPt[0] > 7"),
		     ("$p^{\mu_1}_t>10$" , "MuPt[0] > 10"),
		     ("$p^{\mu_1}_t>17$" , "MuPt[0] > 17") ]:
	    csesNL = [ b for a,b,c in evts(cuta + ROOT.TCut(m))]
	    csesL  = [ b for a,b,c in evts(cutb + ROOT.TCut(m))]
	    print "&".join([n]+map(roundsig,csesNL+csesL)) +"\\\\\\hline"
	print "\\end{tabular}"
	print "\\end{table}"
from CutsCollection import *

print "Requesting two $\mu$, opposite sign"
printTable(qLead,qNoLead,"2 leading b-tagged", "2 btags")
print "Requiring two $\mu$, opposite sign and $MEt<60$, $\sum\limits_{\mu,\,j\,or\,bj} p_t < 100$"
printTable(ptLead,ptNoLead,"2 leading b-tagged", "2 btags")
print "Requesting two $\mu$, opposite sign"
printTable(of4gt2,of4eq2," $>=$ 2 b-tags among 4 leading", " $==$ 2 btags among 4 leading")
print "Requesting one $\mu$"
printTable(smuof4gt2,smuof4eq2," $>=$ 2 b-tags among 4 leading", " $==$ 2 btags among 4 leading")
