

# The files we are going to be loading, along with necessary matching information
files = {
    'data':
        {
            'files': [
                'root://eospublic.cern.ch//eos/opendata/atlas/OutreachDatasets/2020-01-22/4lep/Data/data_A.4lep.root',
                'root://eospublic.cern.ch//eos/opendata/atlas/OutreachDatasets/2020-01-22/4lep/Data/data_B.4lep.root',
                'root://eospublic.cern.ch//eos/opendata/atlas/OutreachDatasets/2020-01-22/4lep/Data/data_C.4lep.root',
                'root://eospublic.cern.ch//eos/opendata/atlas/OutreachDatasets/2020-01-22/4lep/Data/data_D.4lep.root',
                ],
            'nickname': 'data'
        },
    'ggH125_ZZ4lep':
        {
            'files': ['root://eospublic.cern.ch//eos/opendata/atlas/OutreachDatasets/2020-01-22/4lep/MC/mc_345060.ggH125_ZZ4lep.4lep.root'],
            'nickname': 'ggH125_ZZ4lep'
        },
    'ZH125_ZZ4lep':
        {
            'files': ['root://eospublic.cern.ch//eos/opendata/atlas/OutreachDatasets/2020-01-22/4lep/MC/mc_341947.ZH125_ZZ4lep.4lep.root'],
            'nickname': 'ZH125_ZZ4lep'
        },
    'VBFH125_ZZ4lep':
        {
            'files': ['root://eospublic.cern.ch//eos/opendata/atlas/OutreachDatasets/2020-01-22/4lep/MC/mc_344235.VBFH125_ZZ4lep.4lep.root'],
            'nickname': 'VBFH125_ZZ4lep'
        },
    'WH125_ZZ4lep':
        {
            'files': ['root://eospublic.cern.ch//eos/opendata/atlas/OutreachDatasets/2020-01-22/4lep/MC/mc_341964.WH125_ZZ4lep.4lep.root'],
            'nickname': 'WH125_ZZ4lep'
        },
    'ZqqZll':
        {
            'files': ['root://eospublic.cern.ch//eos/opendata/atlas/OutreachDatasets/2020-01-22/4lep/MC/mc_363356.ZqqZll.4lep.root'],
            'nickname': 'ZqqZll'
        },
    # A very weird bug occurs in this file! Awkward fails. No idea what causes this.
    # To repo, run everything, then uncomment this to watch.
    # 'WqqZll':
    #     {
    #         'files': ['root://eospublic.cern.ch//eos/opendata/atlas/OutreachDatasets/2020-01-22/2lep/MC/mc_363358.WqqZll.2lep.root'],
    #         'nickname': 'WqqZll'
    #     },
    'WpqqWmlv':
        {
            'files': ['root://eospublic.cern.ch//eos/opendata/atlas/OutreachDatasets/2020-01-22/2lep/MC/mc_363359.WpqqWmlv.2lep.root'],
            'nickname': 'WpqqWmlv'
        },
    'WplvWmqq':
        {
            'files': ['root://eospublic.cern.ch//eos/opendata/atlas/OutreachDatasets/2020-01-22/2lep/MC/mc_363360.WplvWmqq.2lep.root'],
            'nickname': 'WplvWmqq'
        },
    'WlvZqq':
        {
            'files': ['root://eospublic.cern.ch//eos/opendata/atlas/OutreachDatasets/2020-01-22/2lep/MC/mc_363489.WlvZqq.2lep.root'],
            'nickname': 'WlvZqq'
        },
    'llll':
        {
            'files': ['root://eospublic.cern.ch//eos/opendata/atlas/OutreachDatasets/2020-01-22/4lep/MC/mc_363490.llll.4lep.root'],
            'nickname': 'llll'
        },
    'lllv':
        {
            'files': ['root://eospublic.cern.ch//eos/opendata/atlas/OutreachDatasets/2020-01-22/4lep/MC/mc_363491.lllv.4lep.root'],
            'nickname': 'lllv'
        },
    'llvv':
        {
            'files': ['root://eospublic.cern.ch//eos/opendata/atlas/OutreachDatasets/2020-01-22/4lep/MC/mc_363492.llvv.4lep.root'],
            'nickname': 'llvv'
        },
    'lvvv':
        {
            'files': ['root://eospublic.cern.ch//eos/opendata/atlas/OutreachDatasets/2020-01-22/2lep/MC/mc_363493.lvvv.2lep.root'],
            'nickname': 'lvvv'
        },
    'Zee':
        {
            'files': ['root://eospublic.cern.ch//eos/opendata/atlas/OutreachDatasets/2020-01-22/4lep/MC/mc_361106.Zee.4lep.root'],
            'nickname': 'Zee'
        },
    'Zmumu':
        {
            'files': ['root://eospublic.cern.ch//eos/opendata/atlas/OutreachDatasets/2020-01-22/4lep/MC/mc_361107.Zmumu.4lep.root'],
            'nickname': 'Zmumu'
        },
    'Ztautau':
        {
            'files': ['root://eospublic.cern.ch//eos/opendata/atlas/OutreachDatasets/2020-01-22/4lep/MC/mc_361108.Ztautau.4lep.root'],
            'nickname': 'Ztautau'
        },
}

cms_files = {
    # Not done yet
    'data_2e_7TeV':
        {
            'files': 'cernopendata://16',
            'nickname': 'data_2e_7TeV'
        },
    'data_2mu_7TeV':
        {
            'files': 'cernopendata://17',
            'nickname': 'data_2e_7TeV'
        },
    # Not done yet
    # 'data_2mu_8TeV_B':
    #     {
    #         'files': 'cernopendata://6004',
    #         'nickname': 'data_2mu_8TeV_B',
    #         'backend': 'cms_run1_aod_2'
    #     },
    # Not done yet
    # 'data_2mu_8TeV_C':
    #     {
    #         'files': 'cernopendata://6030',
    #         'nickname': 'data_2mu_8TeV_C'
    #     },
    # Not done yet
    # 'data_2e_8TeV_B':
    #     {
    #         'files': 'cernopendata://6029',
    #         'nickname': 'data_2e_8TeV_B'
    #     },
    'data_2e_8TeV_C':
        {
            'files': 'cernopendata://6003',
            'nickname': 'data_2e_8TeV_C'
        },
    'SMHiggsToZZTo4L_M_125_7TeV':
        {
            'files': 'cernopendata://1507',
            'nickname': 'SMHiggsToZZTo4L_M_125_7TeV'
        },
    'SMHiggsToZZTo4L_M-125_8TeV':
        {
            'files': 'cernopendata://9356',
            'nickname': 'SMHiggsToZZTo4L_M-125_8TeV'
        },
    'ZZTo4mu_mll4_7TeV':
        {
            'files': 'cernopendata://1651',
            'nickname': 'ZZTo4mu_mll4_7TeV'
        },
    'ZZTo4e_mll4_7TeV_II':
        {
            'files': 'cernopendata://1648',
            'nickname': 'ZZTo4e_mll4_7TeV_II'
        },
    'ZZTo2e2mu_mll4_7TeV':
        {
            'files': 'cernopendata://1382',
            'nickname': 'ZZTo2e2mu_mll4_7TeV'
        },
    # Refuses to start at all
    # 'DYJetsToLL_M-50_7TeV':
    #     {
    #         'files': 'cernopendata://1394',
    #         'nickname': 'DYJetsToLL_M_50_7TeV'
    #     },
    'DYJetsToLL_M-10To50_TuneZ2_7TeV':
        {
            'files': 'cernopendata://1393',
            'nickname': 'DYJ_M_10To50_7TeV'
        },
    'DYJetsToLL_M-50_TuneZ2Star_8TeV':
        {
            'files': 'cernopendata://7731',
            'nickname': 'DYJ_M50_8TeV'
        },
    'DYJetsToLL_M-10to50_HT-200to400_TuneZ2star_8TeV':
        {
            'files': 'cernopendata://7727',
            'nickname': 'DYJ_10to50_HT_200to400S_8TeV'
        },
    'DYJetsToLL_M-10to50_HT-400toInf_TuneZ2star_8TeV':
        {
            'files': 'cernopendata://7728',
            'nickname': 'DYJ_10to50_HT_400_8TeV'
        },
    'TTTo2L2Nu2B_7TeV':
        {
            'files': 'cernopendata://1360',
            'nickname': 'TTTo2L2Nu2B_7TeV'
        },
    'ZZTo4mu_8TeV':
        {
            'files': 'cernopendata://10071',
            'nickname': 'ZZTo4mu_8TeV'
        },
    'ZZTo4e_8TeV':
        {
            'files': 'cernopendata://10065',
            'nickname': 'ZZTo4e_8TeV'
        },
    'ZZTo2e2mu_8TeV':
        {
            'files': 'cernopendata://10054',
            'nickname': 'ZZTo2e2mu_8TeV'
        },
    'TTbar_8TeV':
        {
            'files': 'cernopendata://9518',
            'nickname': 'TTbar_8TeV'
        },
}


def get_cms_backend(name: str) -> str:
    '''
    Based on the name, decide on the backend to use
    '''
    if name not in cms_files:
        raise ValueError(f'Unknonw dataset {name}.')

    if 'backend' in cms_files[name]:
        return cms_files[name]['backend']

    return 'cms_run1_aod'
