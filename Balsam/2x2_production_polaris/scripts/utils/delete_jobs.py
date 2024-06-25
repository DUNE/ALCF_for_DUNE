from balsam.api import Job, BatchJob, Site

# for i in range(145,785):
#     Job.objects.filter(tags={"index": f"{i}"}).delete()

# jobs = Job.objects.filter(tags={'workflow':'MiniRun5_1E19_RHC_W_ION_Systematics_mlreco_flow2supera_v0'})
# print(len(jobs))
# jobs.filter(state="FAILED").update(state='AWAITING_PARENTS')

jobs = Job.objects.filter(tags={'workflow':'MiniRun5_1E19_RHC_W_ION_Systematics_mlreco_analysis_v2'})
print(len(jobs))
# jobs.filter(state="FAILED").update(state='AWAITING_PARENTS')
Job.objects.filter(tags={'workflow':'MiniRun5_1E19_RHC_W_ION_Systematics_mlreco_analysis_v2'}).filter(state="FAILED").update(state="RESTART_READY")