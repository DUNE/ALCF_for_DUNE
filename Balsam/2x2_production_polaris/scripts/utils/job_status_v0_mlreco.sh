#!/bin/bash

balsam job ls --tag workflow=MiniRun5_1E19_RHC_W_ION_Systematics_mlreco_flow2supera_v0 > mlreco_supera_jobs.txt
balsam job ls --tag workflow=MiniRun5_1E19_RHC_W_ION_Systematics_mlreco_inference_v0 > mlreco_inference_jobs.txt
balsam job ls --tag workflow=MiniRun5_1E19_RHC_W_ION_Systematics_mlreco_analysis_v0 > mlreco_analysis_jobs.txt