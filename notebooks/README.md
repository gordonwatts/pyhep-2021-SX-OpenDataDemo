# The Demo Notebooks

These are notebooks that contain the raw info for the demos, and some notes (here).

## ATLAS Demo

The $H \rightarrow \ell \ell \ell \ell$ analysis. A short description is found [here](http://opendata.atlas.cern/release/2020/documentation/physics/FL2.html).

Event Selection:

1. Single-electron or Single-Muon Trigger
1. Select Muon and Electron candidate lists:
    * Standard object-selection criteria,
    * loose lepton pT selection
    * loose lepton calorimeter and track based isolation requirements
    * Info can be found in the released [PDF that has details](https://cds.cern.ch/record/2707171/files/ANA-OTRC-2019-01-PUB-updated.pdf) - Table 3.
1. Exactly 4 leptons (electrons or muons)
   * $p_T > 25, 15, 10, 7$ GeV
1. Find the lepton invar mass as close to the Z mass as possible. And the second pair is the other two (Same Flavor, Opposite Sign).
    * There may be a mass window of 66 to 116 applied to these two.
1. The Higgs mass is the 4 lepton combination of the two Z candidates.

The code can be found in a repo that does the above, [here](https://github.com/atlas-outreach-data-tools/atlas-outreach-cpp-framework-13tev/blob/master/Analysis/HZZAnalysis/HZZAnalysis.C) (in C++). And [here is the driver](https://github.com/atlas-outreach-data-tools/atlas-outreach-cpp-framework-13tev/blob/master/Analysis/HZZAnalysis/main_HZZAnalysis.C), which is also contains references to the datasets used.

This should reproduce the plot from MC on the web page linked above.

### Datasets

To make the final plot we need. Run numbers, below, pulled from [here for MC](http://opendata.atlas.cern/release/2020/documentation/datasets/mc.html) and here for data.

* Higgs: Runs 345060 (ggF), 344235 (VBF), 341947 (ZH), 341964 (WH)
* ZZ: Run 363490
* Other: Ugh - there are a lot - see the above driver file to get a complete list.

### Strategy for the analysis

`func_adl` should render events with the trigger applied, loose lepton criteria applied, and at least one lepton of 25 GeV or better. `awkward` will then implement the remaining operations to build the histogram results.
