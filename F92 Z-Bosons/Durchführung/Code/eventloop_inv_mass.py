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
    " =====================\n",
    " Starting the analysis\n",
    " =====================\n",
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

h_invMass = ROOT.TH1D("h_invMass", "Invariant Mass of LO and NLO Leptons; M [GeV/c^{2}]; Entries", 200, 0, 200)
h_invMass2 = ROOT.TH1D()
h_E = ROOT.TH1D("h_E", "Energy of ?", 1000, -100, 10000)

h_cut_flow = ROOT.TH1D("h_cut_flow", "Cut Flow;Selection;events", 20, 0, 20)
label_cuts(
    h_cut_flow,
    [
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        ""
    ]
)

hist = h_invMass
hist2 = h_invMass2

# correct but überflüssig
# def calc_energy(pz, eta):
#     frac = (1 + math.exp(2 * eta)) / (1 - math.exp(2 * eta))
#     return -pz * frac

def calc_inv_mass(E, psquared):
    return E**2 - psquared

def px(pt, phi):
    return pt * math.cos(phi)

def py(pt, phi):
    return pt * math.sin(phi)

def pz(pt, eta):
    return pt * math.sinh(eta)

def calculation(pt, eta, E, phi):
    vE =  (E[0] + E[1]) / 1000
    vpx = (px(pt[0], phi[0]) + px(pt[1], phi[1])) / 1000
    vpy = (py(pt[0], phi[0]) + py(pt[1], phi[1])) / 1000
    vpz = (pz(pt[0], eta[0]) + pz(pt[1], eta[1])) / 1000
    m2 = vE**2 - (vpx**2 + vpy**2 + vpz**2)
    if m2 <= 0:
        print("Ping 1!")
        return None
    return math.sqrt(m2)

def aslist(input) -> list:
    if isinstance(input, float) or isinstance(input, int):
        return [input]
    return input

def calculation2(pt, eta, E, phi):
    p0 = ROOT.TLorentzVector()
    p1 = ROOT.TLorentzVector()
    for i, p in enumerate([p0, p1]):
        p.SetPtEtaPhiE(pt[i] / 1000, eta[i], phi[i], E[i] / 1000)
    ptot = p0 + p1
    m2 = ptot.M2()
    if m2 <= 0:
        print("Ping 2!")
        return None
    return math.sqrt(m2)


# To look at each entry in the tree, loop over it.
# Either loop over a fixed amount of events, or over all entries (nEntries)
if numEvents<0:
    nEntries = myChain.GetEntriesFast()
else:
    nEntries = numEvents

counter1 = 0
counter2 = 0

for jentry in range(0, nEntries):
    # print some info about already processed events
    if jentry % 100000 == 0:
        print("Processed", jentry, "/", nEntries, "events")

    # check number of bytes. If <= 0, then entry does not exist.
    nb = myChain.GetEntry(jentry)
    if nb <= 0: continue

    # real data has mcWeight = 0 while all simulated data has nonzero weight
    # will need to be changed for Monte Carlo events
    if myChain.mcWeight:
        weight = myChain.mcWeight
    else:
        weight = 1

    n = myChain.lep_n
    if n != 2: continue

    # Read variables from the input
    pt  = myChain.lep_pt
    eta = myChain.lep_eta
    E = myChain.lep_E
    phi = myChain.lep_phi

    inv_mass = calculation(pt, eta, E, phi)
    inv_mass2 = calculation2(pt, eta, E, phi)

    if inv_mass is not None:
        hist.Fill(inv_mass, weight)
    if inv_mass2 is not None:
        hist2.Fill(inv_mass2, weight)

    # might be helpful, to access all 32 bits of a 32 bit integer flag individually:

    # for bit in range ( 32 ):
    #     flagBit = lep_flag & (1 << bit)
    #     print flagBit

##########################################################################
#end of the event loop
##########################################################################


### The Wrap-up code (writing the files, etc) goes here
# Let's look at the histogram; create a canvas to draw it on
canvas = ROOT.TCanvas("myCanvas", 'Analysis Plots', 200, 10, 700, 500 )
canvas.cd()
# canvas.SetLogy()
hist2.SetLineColor(ROOT.kRed)
hist.Draw("HIST")
hist2.Draw("HIST same")

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
usr_input = input ("Press any key to continue ")
