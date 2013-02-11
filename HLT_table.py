import ROOT 
ROOT.gROOT.SetBatch()

import DataManager

dm = DataManager.DataManager("..")

c = ROOT.TCanvas("")

i=0
hltBits = {}
for n in dm.HLTs(dm.Names()[0]):
        hltBits[i] = n.HLT
        i += 1

print "\\begin{table}"
print "\\begin{tabular}{|"+"|".join("c" for x in dm.Names())+"|}\\hline"
print "&".join(x for x in dm.Names())+"\\\\\\hline"
for i in hltBits:
        print "\multicolumn{"+str(len(dm.Names()))+"}{|c|}{"+hltBits[i].replace("_","\\_")+"}\\\\\\hline"
        effs = [float(dm.Tree(dset).Draw("JetPt@.size()","(HLTResults&(1<<"+str(i)+"))>0"))/dm.Tree(dset).GetEntries() for dset in dm.Names()]
        print "&".join(("{0:.2%}".format(x)).replace("%","\\%") for x in effs)+ "\\\\\\hline"
print "\\end{tabular}"
print "\\end{table}"
