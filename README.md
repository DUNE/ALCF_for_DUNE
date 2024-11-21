# DUNE Workflows at ANL

This repository currently contains the workflow we have used for running 2x2 detector simulation productions at Argonne National Laboratory on ALCF Polaris Machine.  

It would be helpful to get familiar with the Balsam software [https://balsam.readthedocs.io/en/latest/](https://balsam.readthedocs.io/en/latest/) to understand the workflow scripts, and ALCF Docs for job submission.

Before using these scripts, you would need to create your own Balsam site (due to settings that are user specific or machine specific that are required to run and submit jobs) and place these folders inside of it. Creating a Balsam site: [https://balsam.readthedocs.io/en/latest/tutorials/theta-quickstart/#create-a-balsam-site](https://balsam.readthedocs.io/en/latest/tutorials/theta-quickstart/#create-a-balsam-site)     
In the directory `Balsam/2x2_production_polaris` you will find the following folders:  
- `data` : Contains the source code for 2x2_sim simulation linked to the repository maintained by 2x2 collaboration (https://github.com/DUNE/2x2_sim). The latest tutorial to understand the software is at [https://github.com/DUNE/2x2_sim/wiki/Tutorial-on-running-2x2_sim-Apr2024](https://github.com/DUNE/2x2_sim/wiki/Tutorial-on-running-2x2_sim-Apr2024) and will be updated as when the software does.
- `scripts/apps` : These scripts create the "apps" (Each app defines a job flow that you would like to run, for eg. if you want to setup jobs for the edep sim stage of 2x2, you define the specific environment variables for that stage and edep sim script to run).
- `scripts/workflows`: These scripts create jobs based out of the apps. For every job, we set the indices for the jobs, add unique tags so that it can be queried and specify dependent jobs. These scripts also submit these jobs to run to the ALCF Polaris Machine.
- `scripts/utils`: Some helpful Balsam files for modifying created jobs.
- `specs`: Environment variables required for each production is stored as yaml files and are loaded by the app creation scripts.
- `admin` : contains common scripts for fetching singlarity containers as required, transferring files across facilities and generation of metadata.
- `usage_summary`: Reports on production runs.

Additional information is available in each directory.

Some useful web pages:
Polaris activity for jobs: https://status.alcf.anl.gov/#/polaris.

2x2 sim Github: https://github.com/DUNE/2x2_sim.

NERSC portal for various files with production tags: https://portal.nersc.gov/project/dune/data/2x2.

DUNE larndsim: https://github.com/DUNE/larnd-sim.

DUNE ND CAFMaker: https://github.com/DUNE/ND_CAFMaker/tree/main. 

DUNE standard Record: https://dune.github.io/duneanaobj/classcaf_1_1SRInteraction.html.

For NERSC workflows: https://github.com/lbl-neutrino/fireworks4dune/tree/main.
