# DUNE Workflows at ANL

This repository currently contains the workflow we have used for running 2x2 detector simulation productions at Argonne National Laboratory on ALCF Polaris Machine.  

It would be helpful to get familiar with the Balsam software [https://balsam.readthedocs.io/en/latest/](https://balsam.readthedocs.io/en/latest/) to understand the workflow scripts, and ALCF Docs for job submission.

Before using these scripts, you would need to create your own Balsam site (due to setting that are user specfic or machine specfifc that are required to run and submit jobs) and place these folders inside of it. Creating a Balsam site: [https://balsam.readthedocs.io/en/latest/tutorials/theta-quickstart/#create-a-balsam-site](https://balsam.readthedocs.io/en/latest/tutorials/theta-quickstart/#create-a-balsam-site)
In the directory `Balsam/2x2_production_polaris` you will find the following folders:  
- `data` : Contains the source code for 2x2_sim simulation linked to the repository maintained by 2x2 collaboration (https://github.com/DUNE/2x2_sim). The latest tutorial to understand the softare is at [https://github.com/DUNE/2x2_sim/wiki/Tutorial-on-running-2x2_sim-Apr2024](https://github.com/DUNE/2x2_sim/wiki/Tutorial-on-running-2x2_sim-Apr2024) and will be updated as when the software is.
- `scripts/apps` : These scripts create the "apps" (Each app defines a job flow that you would like to run, for eg. if you want to the edep sim stage of 2x2, you define the environment variables you would like to set for the job, the script to run).
- `scripts/workflows`: These scripts create jobs based out of the apps. For every job, we set the indices for the jobs, add unique tags to the jobs so that it can be queried and specify dependent jobs. These scripts also submit these jobs to run to the ALCF Polaris Machine.
- `scripts/utils`: Some helpful Balsam files for modifying created jobs.
- `specs`: Environment variables required for each production is stored as yaml files and are loaded by the app creation scripts.
- `admin` : contains common scripts for fetching singlarity containers as required, transferring files across facilities and generation of metadata.
- `usage_summary`: Reports on production runs.

Addition information is available in each directory.