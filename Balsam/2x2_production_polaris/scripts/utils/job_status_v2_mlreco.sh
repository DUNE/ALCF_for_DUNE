#!/bin/bash

balsam job ls --tag workflow=MiniRun5_1E19_RHC_W_ION_Systematics_mlreco_inference_v2 > mlreco_inference_jobs_v2.txt
balsam job ls --tag workflow=MiniRun5_1E19_RHC_W_ION_Systematics_mlreco_analysis_v2 > mlreco_analysis_jobs_v2.txt
