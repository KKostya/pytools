import ROOT

twomu = ROOT.TCut("MuCharge[0]*MuCharge[1] <0&& MuGood[0] ==1 && MuGood[1]==1" )

qNoLead = twomu + ROOT.TCut("BJetGood[0]==1 && BJetGood[1]==1" )
qLead = twomu + ROOT.TCut("JetCsv[0]>0.679 && JetCsv[1] > 0.679 && JetGood[0]==1 && JetGood[1]==1" )

ptNoLead = ROOT.TCut("MetEt[0] < 60 && SumPtB < 100") + qNoLead
ptLead = ROOT.TCut("MetEt[0] < 60 && SumPt  < 60") + qLead

of4gt2 = twomu + ROOT.TCut("((JetCsv[0]>0.679?JetGood[0]:0)+(JetCsv[1]>0.679?JetGood[1]:0)+(Alt$(JetCsv[2],0)>0.679?JetGood[2]:0)+(Alt$(JetCsv[3],0)>0.679?JetGood[3]:0))>=2")
of4eq2 = twomu + ROOT.TCut("((JetCsv[0]>0.679?JetGood[0]:0)+(JetCsv[1]>0.679?JetGood[1]:0)+(Alt$(JetCsv[2],0)>0.679?JetGood[2]:0)+(Alt$(JetCsv[3],0)>0.679?JetGood[3]:0))==2")

smuof4gt2 = ROOT.TCut("MuGood[0] == 1 && ((JetCsv[0]>0.679?JetGood[0]:0)+(JetCsv[1]>0.679?JetGood[1]:0)+(Alt$(JetCsv[2],0)>0.679?JetGood[2]:0)+(Alt$(JetCsv[3],0)>0.679?JetGood[3]:0))>=2")
smuof4eq2 = ROOT.TCut("MuGood[0] == 1 && ((JetCsv[0]>0.679?JetGood[0]:0)+(JetCsv[1]>0.679?JetGood[1]:0)+(Alt$(JetCsv[2],0)>0.679?JetGood[2]:0)+(Alt$(JetCsv[3],0)>0.679?JetGood[3]:0))==2")

nobtag   = ROOT.TCut("JetCsv[0] < 0.679 && JetCsv[1] < 0.679")
fstbtag  = ROOT.TCut("JetCsv[0] > 0.679 && JetCsv[1] < 0.679")
sndbtag  = ROOT.TCut("JetCsv[0] < 0.679 && JetCsv[1] > 0.679")
twobtag  = ROOT.TCut("JetCsv[0] > 0.679 && JetCsv[1] > 0.679")
