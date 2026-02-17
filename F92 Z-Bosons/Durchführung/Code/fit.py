# script to determine the Z boson mass
import ROOT
import math
import sys


def gauss(x, par):
    N = par[0]
    m = par[1]
    s = par[2]

    try:
        chi2 = (x[0] - m) * (x[0] - m) / (s*s)
        return N / math.sqrt(2 * math.pi * s*s) * math.exp(-0.5 * chi2)
    except:
        return 0

# you can use https://en.wikipedia.org/wiki/Relativistic_Breit%E2%80%93Wigner_distribution
# with two free parameters: M and Gamma.
# You will need an additional one N for normalization like in the Gaussian
def bw(x, par):
    N = par[0]
    M = par[1]
    Gamma = par[2]
    try:
        gamma = math.sqrt(M*M * (M*M + Gamma*Gamma))
        k = 2 * math.sqrt(2) * M * Gamma * gamma / (math.pi * math.sqrt(M*M + gamma))
        return N * k / ((x[0]*x[0] - M*M)*(x[0]*x[0] - M*M) + M*M * Gamma*Gamma)
    except:
        return 0


mMin = 60. # old: 70.
mMax = 120. # old: 110.

# this removes the statics box from the plot
ROOT.gStyle.SetOptStat(0)

# Create a canvas to draw on later
canvas = ROOT.TCanvas("myCanvas", 'Analysis Plots', 200, 10, 700, 500 )
canvas.cd()

#open the input histogram
rootfile = ROOT.TFile.Open(sys.argv[1], "READ")
tmpHist = rootfile.Get("h_invMass")
tmpHist.GetXaxis().SetRangeUser(mMin,mMax)
tmpHist.SetTitle("Fitting Various Functions to the Z Mass Distribution;M_{ll} [GeV / c^{2}];Entries")
tmpHist.Draw("")

# Create a legend to label the different components of the plot
# https://root.cern.ch/doc/master/classTLegend.html
legend = ROOT.TLegend(0.15, 0.65, 0.4, 0.88)
legend.SetFillColor(0)
legend.SetLineColor(0)

# define a TF1 Gaussian according to our own python function gauss
# https://root.cern.ch/doc/master/classTF1.html
fGauss = ROOT.TF1("fGauss", gauss, mMin, mMax, 3)

fGauss.SetParameter(0, tmpHist.Integral())
fGauss.SetParameter(1, 90.0)
fGauss.SetParameter(2, 4.0)

fGauss.SetLineColor(ROOT.kRed)
fGauss.SetNpx(1000) # sets the amount of sampling points in x range. Do not choose too small for convolution later on
legend.AddEntry(fGauss, "Gauss", "l")


# do the same thing for a Breit-Wigner distribution
fBw = ROOT.TF1("fBw", bw, mMin, mMax, 3)

fBw.SetParameter(0, tmpHist.Integral())
fBw.SetParameter(1, 90.0)
fBw.SetParameter(2, 4.0)

fBw.SetLineColor(ROOT.kMagenta)
fBw.SetNpx(1000) # sets the amount of sampling points in x range. Do not choose too small for convolution later on
legend.AddEntry(fBw, "Breit-Wigner", "l")


# let root perform a convolution of the two functions. It does so by a Fourier transform
# need to set negative x minimum, because Gauss will be centered at 0 and the same range is used on both functions in the convolution
# in principle the order would not matter, but the fit will converge more easily if the distribution centered at 0 comes second
conv = ROOT.TF1Convolution(fBw, fGauss)
conv.SetRange(-20.,mMax)

# convert the TF1Convolution back into a regular TF1 to continue our fitting
# it now has 6 parameters: 0,1,2 from bw and 3,4,5 from gauss
# for the fitting it can make sense to fix some parameters. Both
# parameters for the mean will shift the result along the x axis
# and both for the normalization will scale it along the y axis.
fConv = ROOT.TF1("fConv", conv, mMin, mMax, conv.GetNpar())

fConv.SetLineColor(ROOT.kGreen + 1)
fConv.SetNpx(1000) # sets the amount of sampling points in x range. Do not choose too small for convolution later on
legend.AddEntry(fConv, "Convolution", "l")

fConv.SetParameter(0, tmpHist.Integral())
fConv.SetParameter(1, 90.0)
fConv.SetParameter(2, 4.0)
############
############
fConv.SetParameter(5, 1)    # gauss sigma

fConv.FixParameter(3,1.0) # this would be the normalization of the gauss
fConv.FixParameter(4,0.0) # this would be the mean of the gauss

tmpHist.SetLineWidth(3)
tmpHist.Draw("E")

def dofit(tmpHist, fFunc):
    print("===================================")
    tmpHist.Fit(fFunc)
    print(("chi2/NDF = %f / %f = %f")%(fFunc.GetChisquare(), fFunc.GetNDF(), fFunc.GetChisquare()/fFunc.GetNDF()))
    print("===================================\n")
    fFunc.Draw("SAME")

dofit(tmpHist, fGauss)
dofit(tmpHist, fBw)
dofit(tmpHist, fConv)

def draw_Latex_params(fFunc, name, param_names, start):
    tex = ROOT.TLatex(); tex.SetNDC(True); tex.SetTextSize(0.035); tex.SetTextColor(ROOT.kBlack)
    STEP = 0.05
    tex.DrawLatex(0.65, start, name)
    for i, pname in enumerate(param_names, start = 1):
        if i == 3: i = 5
        text = pname + (" = %.3f #pm %.3f") % (fFunc.GetParameter(i), fFunc.GetParError(i))
        if i == 5: i = 3
        tex.DrawLatex(0.65, start - STEP*i, text)
    tex.DrawLatex(0.65, start - STEP*(len(param_names)+1), "#chi^{2}_{red} = %.1f" %  (fFunc.GetChisquare() / fFunc.GetNDF()))

gauss_pnames = ["M_{Z}", "#sigma"]
bw_pnames = ["M_{Z}", "#Gamma"]
conv_pnames = ["M_{Z}", "#Gamma", "#sigma"]

draw_Latex_params(fGauss, "Gauss Fit", gauss_pnames, 0.85)
draw_Latex_params(fBw, "Breit-Wigner Fit", bw_pnames, 0.60)
draw_Latex_params(fConv, "Convolution Fit", conv_pnames, 0.35)

legend.AddEntry(tmpHist, "Data")
legend.Draw("SAME")


canvas.Update()
#ROOT.TPython.Prompt()
usr_input = input ("Press any key to continue ")

rootfile.Close()
