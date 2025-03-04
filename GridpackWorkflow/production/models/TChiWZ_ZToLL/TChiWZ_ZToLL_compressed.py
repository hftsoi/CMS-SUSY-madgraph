import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *  

import math

baseSLHATable="""
BLOCK MASS  # Mass Spectrum
# PDG code           mass       particle
   1000001     1.00000000E+05   # ~d_L
   2000001     1.00000000E+05   # ~d_R
   1000002     1.00000000E+05   # ~u_L
   2000002     1.00000000E+05   # ~u_R
   1000003     1.00000000E+05   # ~s_L
   2000003     1.00000000E+05   # ~s_R
   1000004     1.00000000E+05   # ~c_L
   2000004     1.00000000E+05   # ~c_R
   1000005     1.00000000E+05   # ~b_1
   2000005     1.00000000E+05   # ~b_2
   1000006     1.00000000E+05   # ~t_1
   2000006     1.00000000E+05   # ~t_2
   1000011     1.00000000E+05   # ~e_L
   2000011     1.00000000E+05   # ~e_R
   1000012     1.00000000E+05   # ~nu_eL
   1000013     1.00000000E+05   # ~mu_L
   2000013     1.00000000E+05   # ~mu_R
   1000014     1.00000000E+05   # ~nu_muL
   1000015     1.00000000E+05   # ~tau_1
   2000015     1.00000000E+05   # ~tau_2
   1000016     1.00000000E+05   # ~nu_tauL
   1000021     1.00000000E+05   # ~g
   1000022     %MLSP%           # ~chi_10
   1000023     %MN2%            # ~chi_20
   1000025     1.00000000E+05   # ~chi_30
   1000035     1.00000000E+05   # ~chi_40
   1000024     %MN2%           # ~chi_1+
   1000037     1.00000000E+05   # ~chi_2+
# DECAY TABLE
#         PDG            Width
DECAY   1000001     0.00000000E+00   # sdown_L decays
DECAY   2000001     0.00000000E+00   # sdown_R decays
DECAY   1000002     0.00000000E+00   # sup_L decays
DECAY   2000002     0.00000000E+00   # sup_R decays
DECAY   1000003     0.00000000E+00   # sstrange_L decays
DECAY   2000003     0.00000000E+00   # sstrange_R decays
DECAY   1000004     0.00000000E+00   # scharm_L decays
DECAY   2000004     0.00000000E+00   # scharm_R decays
DECAY   1000005     0.00000000E+00   # sbottom1 decays
DECAY   2000005     0.00000000E+00   # sbottom2 decays
DECAY   1000006     0.00000000E+00   # stop1 decays
DECAY   2000006     0.00000000E+00   # stop2 decays
DECAY   1000011     0.00000000E+00   # selectron_L decays
DECAY   2000011     0.00000000E+00   # selectron_R decays
DECAY   1000012     0.00000000E+00   # snu_elL decays
DECAY   1000013     0.00000000E+00   # smuon_L decays
DECAY   2000013     0.00000000E+00   # smuon_R decays
DECAY   1000014     0.00000000E+00   # snu_muL decays
DECAY   1000015     0.00000000E+00  # stau_1 decays
DECAY   2000015     0.00000000E+00   # stau_2 decays
DECAY   1000016     0.00000000E+00   # snu_tauL decays
DECAY   1000021     0.00000000E+00   # gluino decays
DECAY   1000022     0.00000000E+00   # neutralino1 decays
DECAY   1000023     1.00000000E-1   # neutralino2 decays
    0.00000000E+00   3    1000022   11   -11
    1.00000000E+00   2    1000022   23
DECAY   1000024     1.00000000E-1   # chargino1+ decays
    0.00000000E+00   3    1000022   12   -11
    1.00000000E+00   2    1000022   24
DECAY   1000025     0.00000000E+00   # neutralino3 decays
DECAY   1000035     0.00000000E+00   # neutralino4 decays
DECAY   1000037     0.00000000E+00   # chargino2+ decays
"""

generator = cms.EDFilter("Pythia8GeneratorFilter",
    maxEventsToPrint = cms.untracked.int32(1),
    pythiaPylistVerbosity = cms.untracked.int32(1),
    filterEfficiency = cms.untracked.double(1.0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(13000.),
    RandomizedParameters = cms.VPSet(),
)

model = "TChiWZ_ZToLL"
# weighted average of matching efficiencies for the full scan
# must equal the number entered in McM generator params
mcm_eff = 0.506
# Scan contains 22,750,000 events

def matchParams(mass):
  if mass < 124: return 76,0.64
  elif mass < 151: return 76, 0.6
  elif mass < 176: return 76, 0.57
  elif mass < 226: return 76, 0.54
  elif mass < 326: return 76, 0.51
  elif mass < 451: return 76, 0.48
  elif mass < 651: return 76, 0.45
  else: return 76, 0.42

# Parameters that define the grid in the bulk and diagonal
class gridBlock:
  def __init__(self, xmin, xmax, xstep, ystep):
    self.xmin = xmin
    self.xmax = xmax
    self.xstep = xstep
    self.ystep = ystep

# Number of events: min(goalLumi*xsec, maxEvents) (always in thousands)
diagStep = 100
maxDM = 60
extras = range(10,51,10)
extras.extend([0.6,0.8,1,1.5,2.,3,5,7.5,15])

scanBlocks = []
scanBlocks.append(gridBlock(100, 501, 25, 25))
minDM = 60
ymin, ymed, ymax = 0, 0, 501

# Number of events for mass point, in thousands
def events(dm):
  if dm<=50: return 100
  else: return 50

# -------------------------------
#    Constructing grid

cols = []
xmin, xmax = 9999, 0
for block in scanBlocks:
  for mx in range(block.xmin, block.xmax, block.xstep):
    xmin = min(xmin, block.xmin)
    xmax = max(xmax, block.xmax)
    col = []
    my = 0
    begDiag = max(ymed, mx-maxDM)
    if(my !=  mx-minDM and mx-minDM <= ymax) or (my ==  mx-minDM):
      #if mx-minDM>=0:
      #  my = mx-minDM
      #  nev = events(mx-my)
      #  col.append([mx,my, nev])
      for ydm in extras:
        nev = events(ydm)
        if (mx-ydm <= ymax) and (mx-ydm>=0): col.append([mx,mx-ydm, nev])
    cols.append(col)

mpoints = []
for col in cols: mpoints.extend(col)

for point in mpoints:
    mn2, mlsp = point[0], point[1]
    qcut, tru_eff = matchParams(mn2)
    wgt = point[2]*(mcm_eff/tru_eff)
    
    if mlsp==0: mlsp = 1
    slhatable = baseSLHATable.replace('%MN2%','%e' % mn2)
    slhatable = slhatable.replace('%MLSP%','%e' % mlsp)
    
    basePythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock, 
        JetMatchingParameters = cms.vstring(
            'JetMatching:setMad = off',
            'JetMatching:scheme = 1',
            'JetMatching:merge = on',
            'JetMatching:jetAlgorithm = 2',
            'JetMatching:etaJetMax = 5.',
            'JetMatching:coneRadius = 1.',
            'JetMatching:slowJetPower = 1',
            'JetMatching:qCut = %.0f' % qcut, #this is the actual merging scale
            'JetMatching:nQmatch = 5', #4 corresponds to 4-flavour scheme (no matching of b-quarks), 5 for 5-flavour scheme
            'JetMatching:nJetMax = 2', #number of partons in born matrix element for highest multiplicity
            'JetMatching:doShowerKt = off', #off for MLM matching, turn on for shower-kT matching
            '23:onMode = off',
            '23:onIfAny = 11 13 15',
            '23:mMin = 0.1',
            '24:mMin = 0.1',
            'Check:abortIfVeto = on',
        ), 
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings', 
                                    'JetMatchingParameters'
        )
    )

    generator.RandomizedParameters.append(
        cms.PSet(
            ConfigWeight = cms.double(wgt),
            GridpackPath =  cms.string('/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/madgraph/V5_2.6.5/sus_sms/SMS-C1N2_v2/SMS-C1N2_mC1-%i_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz' % mchi),
            ConfigDescription = cms.string('%s_%i_%i' % (model, mn2, mlsp)),
            SLHATableForPythia8 = cms.string('%s' % slhatable),
            PythiaParameters = basePythiaParameters,
        ),
    )
