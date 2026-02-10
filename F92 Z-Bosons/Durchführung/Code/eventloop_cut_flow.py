# Lines beginning with "#" are comments in python.
# Start your program by importing Root and some other handy modules
import ROOT
import math
import sys
import os
import os.path
# from scipy.constants import c
# The argparse module makes it easy to write user-friendly command-line interfaces.
import argparse

# we add the flags -f and -n to the scripts, so we can pass arguments in the command line:
# e.g.   python eventloop.py -f someFile.root -n 10
parser = argparse.ArgumentParser(description='Analysis of Z events.')
parser.add_argument('-f', metavar='inputFile', type=str, nargs=1, help='Input ROOT file', required=True)
parser.add_argument('-n', metavar='numEvents', type=int, nargs=1, help='Number of events to process (default all)')

args = parser.parse_args()
fileName = str(args.f[0])
numEvents = -1
if args.n != None :
    numEvents = int(args.n[0])

# from now on, fileName contains the string with the path to our input file and
# numEvents the integer of events we want to process

# Some ROOT global settings and styling
ROOT.TH1.SetDefaultSumw2()

# The execution starts here
print(
    "\n",
    " ================================\n",
    " Starting the analysis (cut flow)\n",
    " ================================\n",
    sep = ""
)

# Open the input file. The name can be hardcoded, or given from commandline as argument
myfile = None
if os.path.isfile(fileName) and os.access(fileName, os.R_OK):
    myfile = ROOT.TFile(fileName)
else:
    sys.exit("Error: Input file does not exist or is not readable")

print("Opened file %s"%myfile.GetName())

# Now you have access to everything you can also see by using the TBrowser
# Load the tree containing all the variables
myChain = ROOT.gDirectory.Get( 'mini' )

# Open an output file to save your histograms in (we build the filename such that it contains the name of the input file)
# RECREATE means, that an already existing file with this name would be overwritten
outfile = ROOT.TFile.Open("analysis_"+myfile.GetName().split('/')[-1], "RECREATE")
outfile.cd()

def label_cuts(hist, cut_names: list) -> None:
    for i, cut in enumerate(cut_names, start = 1):
        hist.GetXaxis().SetBinLabel(i, cut)

# Book histograms within the output file
hVertexDist = ROOT.TH1D("hVertexDist", "Distribution of the interaction vertex along the z-axis; z [mm]; Entries", 1000, -300, 300)
hLepNum = ROOT.TH1D("hLepNum", "Number of Leptons in the Final State; n_{Lepton}; Entries", 6, 0, 6)
hLepEta = ROOT.TH1D("hLepEta", "Pseudorapidity of Leptons; #eta; Entries", 1000, -3, 3)
hLepPt = ROOT.TH1D("hLepPt", "Transverse Momentum of Leptons ; p_{T} [GeV]; Entries", 1000, 0, 160)
hLepPhi = ROOT.TH1D("hLepPhi", "Azimuthal Angle of Leptons; #phi; Entries", 1000, -4, 4)

h_invMass = ROOT.TH1D(
    "h_invMass",
    "Invariant Mass of LO and NLO Leptons (MC, Z_{#tau#tau}); M [GeV/c^{2}]; Entries",
    1000, 60, 120
)
h_E = ROOT.TH1D("h_E", "Energy of ?", 1000, -100, 10000)

h_ptcone = ROOT.TH1D(
    "h_ptcone",
    "Distribution of Transverse Momentum Isolation of Leptons; p_{T,cone}/p_{T}; Entries",
    1000, -0.01, 1
)

h_cut_flow = ROOT.TH1D("h_cut_flow", "Cut Flow of Event Filtering;Selection;Events", 13, 0, 13)
cut_names = [
    "All",
    "Weights",
    "Trigger",
    "GRL",
    "Vertex",
    "#ge 2 Leptons",
    "PDGID",
    "Charge",
    "p_T Cut",
    "E_T Isolation",
    "p_T Isolation",
    "Tight ID",
    "Z Mass"
]
label_cuts(h_cut_flow, cut_names)
h_cut_flow.SetStats(0)

def aslist(input) -> list:
    if isinstance(input, float) or isinstance(input, int):
        return [input]
    return input

def calc_Zmass(pt, eta, E, phi):
    p0 = ROOT.TLorentzVector()
    p1 = ROOT.TLorentzVector()
    for i, p in enumerate([p0, p1]):
        p.SetPtEtaPhiE(pt[i] / 1000, eta[i], phi[i], E[i] / 1000)
    ptot = p0 + p1
    m2 = ptot.M2()
    if m2 <= 0:
        return None
    return math.sqrt(m2)

def get_mcWeight(myChain) -> float:
    # real data has mcWeight = 0 while all simulated data has nonzero weight
    # will need to be changed for Monte Carlo events
    if myChain.mcWeight:
        weight = myChain.mcWeight
    else:
        weight = 1
    return weight

# The following functions will return wether the event passes or fails the cut
def cut_all(myChain) -> bool:
    return True
def cut_weight(myChain) -> bool:
    return True
def cut_trigger(myChain) -> bool:
    return myChain.trigE or myChain.trigM
def cut_GRL(myChain) -> bool:
    return myChain.passGRL
def cut_vertex(myChain) -> bool:
    return myChain.hasGoodVertex
def cut_two_leptons(myChain) -> bool:
    return myChain.lep_n == 2
lepton_ids = {11, 12, 13, 14}    # neutrinos {15, 16, 16}
def cut_PDGID(myChain) -> bool:
    lep_type_vector = myChain.lep_type
    return all(lep_type in lepton_ids for lep_type in lep_type_vector)
def cut_charge(myChain) -> bool:
    lep_charge_vector = myChain.lep_charge
    return lep_charge_vector[0] != lep_charge_vector[1]
def cut_pt(myChain) -> bool:
    lep_pt_vector = myChain.lep_pt
    return all(pt / 1000 >= 25 for pt in lep_pt_vector)
def cut_Et_isolation(myChain) -> bool:
    CUTOFF = 5
    return all(Etcone / E <= CUTOFF for Etcone, E in zip(myChain.lep_etcone20, myChain.lep_E))
def cut_pt_isolation(myChain) -> bool:
    CUTOFF = 5
    return all(ptcone / pt <= CUTOFF for ptcone, pt in zip(myChain.lep_ptcone30, myChain.lep_pt))
def cut_tightID(myChain) -> bool:
    return all(bool((flag & 2**9)) for flag in myChain.lep_flag)
def cut_Zmass(myChain) -> bool:
    MIN_CUTOFF = 60
    MAX_CUTOFF = 120
    Zmass = calc_Zmass(myChain.lep_pt, myChain.lep_eta, myChain.lep_E, myChain.lep_phi)
    return (MIN_CUTOFF <= Zmass <= MAX_CUTOFF)

functions = [
    cut_all,
    cut_weight,
    cut_trigger,
    cut_GRL,
    cut_vertex,
    cut_two_leptons,
    cut_PDGID,
    cut_charge,
    cut_pt,
    cut_Et_isolation,
    cut_pt_isolation,
    cut_tightID,
    cut_Zmass
]

def all_filters(myChain, hist) -> bool:
    for i, filter_func in enumerate(functions, start = 1):
        if filter_func(myChain):
            hist.AddBinContent(i, get_mcWeight(myChain))
        else:
            return False
    return True


# To look at each entry in the tree, loop over it.
# Either loop over a fixed amount of events, or over all entries (nEntries)
if numEvents<0:
    nEntries = myChain.GetEntriesFast()
else:
    nEntries = numEvents

for jentry in range(0, nEntries):
    # print some info about already processed events
    if jentry % (nEntries//10) == 0:
        print("Processed", jentry, "/", nEntries, "events")

    # check number of bytes. If <= 0, then entry does not exist.
    nb = myChain.GetEntry(jentry)
    if nb <= 0: continue

    weight = get_mcWeight(myChain)

    if all_filters(myChain, h_cut_flow):
        Zmass = calc_Zmass(myChain.lep_pt, myChain.lep_eta, myChain.lep_E, myChain.lep_phi)
        h_invMass.Fill(Zmass, weight)

    # for a, b in zip(myChain.lep_ptcone30, myChain.lep_pt):
    #     ratio = a / b
    #     if ratio != 0:
    #         h_ptcone.Fill(ratio, weight)


##########################################################################
#end of the event loop
##########################################################################


### The Wrap-up code (writing the files, etc) goes here
# Let's look at the histogram; create a canvas to draw it on
canvas = ROOT.TCanvas("myCanvas", 'Analysis Plots', 200, 10, 700, 500 )
canvas.cd()
# canvas.SetLogy()
# h_cut_flow.Draw("HIST")
h_invMass.Draw("HIST L")

canvas.Update()
#########################################################################

outfile.cd()
print("Writing output to %s"%outfile.GetName())
outfile.Write()

#useful command to pause the execution of the code. Allows to see the plot before python finishes
#ROOT.TPython.Prompt()
# MW: 1/9/2022: Caution here. In a multi-python build, libROOTTPython is only built for the highest
# Python version. Bottomline: if you run TPython from Python, make sure your Python version is the
# one that TPython was built for. Hence, instead we use standard python now instead.
usr_input = input("Press any key to continue ")
