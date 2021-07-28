# pyhep-2021-SX-OpenDataDemo
 Talk and practice notebooks for the PyHEP 2021 Proposed Talk
 
 [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5142261.svg)](https://doi.org/10.5281/zenodo.5142261)
 
**NOTE** This repository was just just at the time of the talk at PyHEP. Improvements to these notebooks, and backend software, are getting tracked in [another repository](https://github.com/iris-hep/opendata-higgs-discovery) in the [iris-hep organization](https://github.com/iris-hep). There should be no further modificaitons to this repository!

## Using

You can find the final notebooks used in the talk in the [talks](tree/main/talk) directory. The [notebooks](tree/main/notebooks) directory contains practice notebooks used to develop concepts for the talk. They are not necessarily well documented. The talk directory contains information on what notebooks are availible.

If you were to ask - what big thing is missing? The answer would be the determination of systematic errors. The collaborations, of course, paid extensive attention to this. However, it requires a lot more data, studies, and tests, and so does note appear in these Open Data demos.

### ServiceX for the demo

You'll need a `servicex.yaml` file in your home directory that contains something like the following:

```
api_endpoints:
  - endpoint: http://xxx.org
    type: open_uproot
  - endpoint: http://yyy.org
    type: cms_run1_aod


backend_types:
  - type: open_uproot
    return_data: parquet
  - type: cms_run1_aod
    return_data: root
```

Please get in touch with us to get the address of the open instances running `ServiceX`.

### Setting up the environment

Setup your environment:

1. This has been run under python 3.9.6. It should work with anything that is 3.7 or greater.

1. Check out this repostiory locally, and check out the [coffea patched repository locally](https://github.com/gordonwatts/coffea).
1. For the `coffea` repository, check out the branch [pr_servicex_flat_root_files](https://github.com/gordonwatts/coffea/tree/pr_servicex_flat_root_files). For this package use the head.
1. `python -m venv .venv`, and activate the new environment.
1. `pip install -r requirements.txt`
1. In the root directory of the checked out `coffea` package, run `pip install -e[servicex]`.

From there you can start `jupyter-lab`.

If you are on windows, you'll need to make sure LongPathNames are turned on - as some of the CMS pathnames are longer than... well... heck.

### Running on binder

It is not currently possible to run on `binder` as `ServiceX` uses a non-standard port to download data.


## Plans

The [issues](/../../issues) describes a list of issues that were encountered as this repository was built. As they are worked on, they will slowly be incorporated into this repostory.
