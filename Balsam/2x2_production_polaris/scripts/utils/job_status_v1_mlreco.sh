#!/bin/bash

balsam job ls --tag workflow=MiniRun5_1E19_RHC_W_ION_Systematics_mlreco_v1_flow2supera_v1_v1 > mlreco_v1_supera_jobs.txt
balsam job ls --tag workflow=MiniRun5_1E19_RHC_W_ION_Systematics_mlreco_v1_inference_v1_v1 > mlreco_v1_inference_jobs.txt
balsam job ls --tag workflow=MiniRun5_1E19_RHC_W_ION_Systematics_mlreco_v1_analysis_v1_v1 > mlreco_v1_analysis_jobs.txt