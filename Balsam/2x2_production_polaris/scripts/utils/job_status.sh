#!/bin/bash

balsam job ls --tag workflow=MiniRun5_1E19_RHC_W_ION_Systematics_larnd_v0 > larnd_jobs.txt
balsam job ls --tag workflow=MiniRun5_1E19_RHC_W_ION_Systematics_flow_v0 > flow_jobs.txt
balsam job ls --tag workflow=MiniRun5_1E19_RHC_W_ION_Systematics_plot_v0 > plot_jobs.txt
