import awkward as ak
import numpy as np
from coffea import hist
from coffea.processor.servicex import Analysis, LocalExecutor
from func_adl import ObjectStream


def apply_event_cuts (source: ObjectStream) -> ObjectStream:
    '''Event level cuts for the analysis. Keep from sending data that we aren't going to need at all in the end.
    '''
    return (source
        .Where(lambda e: e.trigE or e.trigM))

def good_leptons(source: ObjectStream) -> ObjectStream:
    '''Select out all good leptons from each event. Return their pt, eta, phi, and E, and other
    things needed downstream.

    Because uproot doesn't tie toegher the objects, we can't do any cuts at this point.
    '''
    return source.Select(lambda e:
        {
            'lep_pt': e.lep_pt,
            'lep_eta': e.lep_eta,
            'lep_phi': e.lep_phi,
            'lep_energy': e.lep_E,
            'lep_charge': e.lep_charge,
            'lep_ptcone30': e.lep_ptcone30,
            'lep_etcone20': e.lep_etcone20,
            'lep_typeid': e.lep_type,
            'lep_trackd0pvunbiased': e.lep_trackd0pvunbiased,
            'lep_tracksigd0pvunbiased': e.lep_tracksigd0pvunbiased,
            'lep_z0': e.lep_z0,
            # 'mcWeight': e.mcWeight,
            # 'scaleFactor': e.scaleFactor_ELE*e.scaleFactor_MUON*e.scaleFactor_LepTRIGGER*e.scaleFactor_PILEUP,
        }) \
        .AsParquetFiles('junk.parquet')

class ATLAS_Higgs_4L(Analysis):
    '''Run the 4 Lepton analysis on ATLAS educational ntuples
    '''
    @staticmethod
    def process(events):
        from collections import defaultdict

        import awkward as ak

        sumw = defaultdict(float)
        mass_hist = hist.Hist(
            "Events",
            hist.Cat("channel", "Channel"),
            hist.Bin("mass", "$Z_{ee}$ [GeV]", 60, 60, 180),
        )
        # weight = events.scaleFactor*events.mcWeight
        weight = 1.0

        dataset = events.metadata['dataset']
        leptons = events.lep

        # Good electon selection
        electrons_mask = ((leptons.typeid == 11)
            & (leptons.pt > 7000.0)
            & (abs(leptons.eta) <2.47)
            & (leptons.etcone20 / leptons.pt < 0.3)
            & (leptons.ptcone30 / leptons.pt < 0.3)
            & (abs(leptons.trackd0pvunbiased) / leptons.tracksigd0pvunbiased < 5)
            & (abs(leptons.z0*np.sin(leptons.theta)) < 0.5)
        )

        electrons_good = leptons[electrons_mask]

        # Good muon selection
        muon_mask = ((leptons.typeid == 13)
            & (leptons.pt > 5000.0)
            & (abs(leptons.eta) <2.5)
            & (leptons.etcone20 / leptons.pt < 0.3)
            & (leptons.ptcone30 / leptons.pt < 0.3)
            & (abs(leptons.trackd0pvunbiased) / leptons.tracksigd0pvunbiased < 3)
            & (abs(leptons.z0*np.sin(leptons.theta)) < 0.5)
        )

        muons_good = leptons[muon_mask]

        # In order to cut in sorted lepton pt, we have to rebuild a lepton array here
        leptons_good = ak.concatenate((electrons_good, muons_good), axis=1)
        leptons_good_index = ak.argsort(leptons_good.pt, ascending=False)
        leptons_good_sorted = leptons_good[leptons_good_index]

        # Event level cuts now that we know the good leptons
        # - We need to look at 4 good lepton events only
        # - We need same flavor, so check for even numbers of each flavor
        # - all charges must be balenced
        event_mask = (
            (ak.num(leptons_good_sorted) == 4)
            & ((ak.num(electrons_good) == 0) | (ak.num(electrons_good) == 2) | (ak.num(electrons_good) == 4))
            & ((ak.num(muons_good) == 0) | (ak.num(muons_good) == 2) | (ak.num(muons_good) == 4))
            & (ak.sum(electrons_good.charge, axis=1) == 0)
            & (ak.sum(muons_good.charge, axis=1) == 0)
        )

        # Next, we need to cut on the pT for the leading, sub-leading, and sub-sub-leading lepton
        leptons_good_preselection = leptons_good[event_mask]
        event_good_lepton_mask = (
            (leptons_good_preselection[:,0].pt > 25000.0)
            & (leptons_good_preselection[:,1].pt > 15000.0)
            & (leptons_good_preselection[:,2].pt > 10000.0)
        )

        # Now, we need to rebuild the good muon and electron lists with those selections
        muons_analysis = muons_good[event_mask][event_good_lepton_mask]
        electrons_analysis = electrons_good[event_mask][event_good_lepton_mask]

        # Lets do eemumu events - as there are no permutations there.abs
        # At this point if there are two muons, there must be two electrons
        eemumu_mask = (ak.num(muons_analysis) == 2)
        muon_eemumu = muons_analysis[eemumu_mask]
        electrons_eemumu = electrons_analysis[eemumu_mask]
        z1_eemumu = muon_eemumu[:,0] + muon_eemumu[:,1]
        z2_eemumu = electrons_eemumu[:,0] + electrons_eemumu[:,1]
        h_eemumu = z1_eemumu + z2_eemumu

        sumw[dataset] += len(h_eemumu)
        mass_hist.fill(
            channel='eemumu',
            mass=h_eemumu.mass/1000.0,
            weight=weight*np.ones(len(h_eemumu.mass))
        )

        # Next, eeee. For this we have to build permutations and select the best one
        def four_leptons_one_flavor(same_flavor_leptons, channel: str):
            fl_positive = same_flavor_leptons[same_flavor_leptons.charge > 0]
            fl_negative = same_flavor_leptons[same_flavor_leptons.charge < 0]
            fl_pairs = ak.cartesian((fl_positive, fl_negative))
            # fl_pairs_args = ak.argcartesian((fl_positive, fl_negative))
            zs = fl_pairs["0"] + fl_pairs["1"]

            delta = abs((91.18*1000.0) - zs.mass[:])
            closest_masses = np.min(delta, axis=-1)
            the_closest = (delta == closest_masses)
            the_furthest = the_closest[:,::-1]

            # mass_hist.fill(
            #     channel=f'{channel}-z1',
            #     mass=ak.flatten(zs[the_closest].mass/1000.0)
            # )
            # mass_hist.fill(
            #     channel=f'{channel}-z2',
            #     mass=ak.flatten(zs[the_furthest].mass/1000.0)
            # )
            h_eeee = zs[the_closest] + zs[the_furthest]
            sumw[dataset] += len(h_eeee)
            mass_hist.fill(
                channel=channel,
                mass=ak.flatten(h_eeee.mass/1000.0),
                weight=weight*np.ones(len(h_eeee.mass)),
            )

        four_leptons_one_flavor(electrons_analysis[(ak.num(electrons_analysis) == 4)],
                                'eeee')
        four_leptons_one_flavor(muons_analysis[(ak.num(muons_analysis) == 4)],
                                'mumumumu')
        
        # Testing why the above closest and furthers works. NO IDEA.
        # for i in range(10):
        #     print(f'  -> {i}')
        #     print('      ', zs[the_closest][i].mass)
        #     print('      ', ele_pairs_args[the_closest][i][0])
        #     print('      ', zs[the_furthest][i].mass)
        #     print('      ', ele_pairs_args[the_furthest][i][0])

        # close_parings = ele_pairs_args[the_closest][:][0]
        # far_parings = ele_pairs_args[the_furthest][:][0]

        # close_positive, close_negative = ak.unzip(close_parings)
        # far_positive, far_negative = ak.unzip(far_parings)

        # print(ak.sum(close_positive == far_positive))
        # print(ak.sum(close_negative == far_negative))
        
        return {
            "sumw": sumw,
            "mass": mass_hist,
        }

async def run_analysis(ds_name: str):
    '''
    Run on a known analysis file/files and return the result.
    Should be fine to start many of these at once.
    '''

    # Build the query

    analysis = ATLAS_Higgs_4L()
    # TODO: It would be good if datatype was determined automagically (there is enough info)
    executor = LocalExecutor(datatype='parquet')

    datasource = make_ds('ggH125_ZZ4lep', leptons)

    async def run_updates_stream(accumulator_stream):
    global first

    count = 0
    async for coffea_info in accumulator_stream:
        count += 1
        print(count, coffea_info)
    return coffea_info

    # Why do I need run_updates_stream, why not just await on execute (which fails with async gen can't).
    # Perhaps something from aiostream can help here?
    result = await run_updates_stream(executor.execute(analysis, datasource))
