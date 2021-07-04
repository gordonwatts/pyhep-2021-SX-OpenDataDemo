import asyncio
from typing import List, Union

import awkward as ak
import numpy as np
from coffea import hist
from coffea.processor.servicex import Analysis, DataSource, LocalExecutor
from func_adl import ObjectStream
from func_adl_servicex import ServiceXSourceUpROOT
from servicex.servicex import ServiceXDataset


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
            'mcWeight': e.mcWeight,
            'scaleFactor': e.scaleFactor_ELE*e.scaleFactor_MUON*e.scaleFactor_LepTRIGGER*e.scaleFactor_PILEUP,
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
            hist.Cat("dataset", "Dataset"),
            hist.Bin("mass", "$Z_{ee}$ [GeV]", 60, 60, 180),
        )

        dataset = events.metadata['dataset']
        leptons = events.lep

        weight =  ak.Array(np.ones(len(events.scaleFactor))) if events.metadata['is_data'] \
            else events.scaleFactor*events.mcWeight

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
            channel=r'$ee\mu\mu$',
            mass=h_eemumu.mass/1000.0,
            dataset=dataset,
            weight=weight[eemumu_mask]
        )

        # Next, eeee. For this we have to build permutations and select the best one
        def four_leptons_one_flavor(same_flavor_leptons, event_weights, channel: str):
            fl_positive = same_flavor_leptons[same_flavor_leptons.charge > 0]
            fl_negative = same_flavor_leptons[same_flavor_leptons.charge < 0]
            fl_pairs = ak.cartesian((fl_positive, fl_negative))
            # fl_pairs_args = ak.argcartesian((fl_positive, fl_negative))
            zs = fl_pairs["0"] + fl_pairs["1"]

            delta = abs((91.18*1000.0) - zs.mass[:])
            closest_masses = np.min(delta, axis=-1)
            the_closest = (delta == closest_masses)
            the_furthest = the_closest[:,::-1]

            h_eeee = zs[the_closest] + zs[the_furthest]
            sumw[dataset] += len(h_eeee)
            mass_hist.fill(
                channel=channel,
                mass=ak.flatten(h_eeee.mass/1000.0),
                dataset=dataset,
                weight=event_weights,
            )

        four_leptons_one_flavor(electrons_analysis[(ak.num(electrons_analysis) == 4)],
                                weight[(ak.num(electrons_analysis) == 4)],
                                '$eeee$')
        four_leptons_one_flavor(muons_analysis[(ak.num(muons_analysis) == 4)],
                                weight[(ak.num(muons_analysis) == 4)],
                                '$\\mu\\mu\\mu\\mu$')
        
        return {
            "sumw": sumw,
            "mass": mass_hist,
        }


def make_ds(name: str, query: ObjectStream):
    '''Create a ServiceX Datasource for a particular ATLAS Open data file
    '''
    from utils import files
    is_data = name == 'data'
    datasets = [ServiceXDataset(files[name]['files'], backend_type='open_uproot', image='sslhep/servicex_func_adl_uproot_transformer:pr_fix_awk_bug')]
    return DataSource(query=query, metadata={'dataset': name, 'is_data': is_data}, datasets=datasets)


async def run_atlas_4l_analysis(ds_names: Union[str,List[str]]):
    '''
    Run on a known analysis file/files and return the result.
    Should be fine to start many of these at once.

    ds_names are names in utils, or "*" which means everything.
    '''
    # Parse the dataset if need be.
    if isinstance(ds_names, str):
        if ds_names != '*':
            raise Exception('DS Name should be a list or a * for everything')
        from utils import files
        ds_names = list(files.keys())

    # Create the query
    ds = ServiceXSourceUpROOT('cernopendata://dummy',  "mimi", backend='open_uproot')
    ds.return_qastle = True
    leptons = good_leptons(apply_event_cuts(ds))

    # Get data source for this run
    # TODO: Why do I need to tell it the datatype?
    executor = LocalExecutor(datatype='parquet')
    datasources = [make_ds(ds_name, leptons) for ds_name in ds_names]

    # Create the analysis and we can run from there.
    analysis = ATLAS_Higgs_4L()

    async def run_updates_stream(accumulator_stream, name):
        '''Run to get the last item in the stream'''
        coffea_info = None
        try:
            async for coffea_info in accumulator_stream:
                pass
        except Exception as e:
            raise Exception(f'Failure while processing {name}') from e
        return coffea_info

    # Why do I need run_updates_stream, why not just await on execute (which fails with async gen can't).
    # Perhaps something from aiostream can help here?
    all_plots = await asyncio.gather(*[run_updates_stream(executor.execute(analysis, source), source.metadata['dataset']) for source in datasources])

    # Combine the plots
    all_plots_mass = [p['mass'] for p in all_plots]
    mass = all_plots_mass[0]
    for p in all_plots_mass[1:]:
        mass.add(p)

    return mass
