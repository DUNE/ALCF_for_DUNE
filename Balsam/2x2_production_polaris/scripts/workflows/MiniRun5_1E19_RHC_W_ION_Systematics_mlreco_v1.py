from balsam.api import ApplicationDefinition, BatchJob, Job, Site
import yaml

#Machine variables
#########################
queue = "debug"          #
project="ALCF_for_DUNE" #
job_mode="mpi"          #
#########################

#build larndsim again in the venv after changing the constant

#release of jobs
#first 16 jobs,
#then 10 jobs of 128 each

#need to filter/tag submit index for jobs while submitting otherwise balsam submits
#all of the jobs 

#default prod
cpu_packing_count = 1
gpu_packing_count = 1

name = 'MiniRun5_1E19_RHC_W_ION_Systematics_mlreco_v1'

site_name = "2x2_production_polaris"

runs = ["submit_all_cpu"]

#v0 wion = 22.7
#v1 wion = 25.1

version = "v3"

"""
Functions
"""


begin_index = 1
spill_size = 128
end_index = 2
wall_time_min = 60
num_nodes = 1


def create_jobs(app_id, size, node_packing_count):

    for i in range(size):
        Job.objects.create( app_id=app_id,
                            site_name=site_name,
                            workdir=f"workdir/{version}_{i}_{app_id}",
                            node_packing_count=node_packing_count,
                            tags={"workflow": f"{name}_{app_id}_{version}", "index":f"{i}"},
                            data={"i": i})

def create_single_dependent_job(app_id, i, parent_ids, node_packing_count, start):

    Job.objects.create( app_id=app_id,
                        site_name=site_name,
                        workdir=f"workdir/{version}_{i}_{app_id}",
                        node_packing_count=node_packing_count,
                        tags={"workflow": f"{name}_{app_id}_{version}", "index":f"{i}", "job_start":f"{start}"},
                        data={"i": i},
                        parent_ids=parent_ids)

def submit_filtered_jobs(app_id, num_nodes=1, wall_time_min = 60):

    site = Site.objects.get(site_name)

    BatchJob.objects.create(
        num_nodes=num_nodes,
        wall_time_min=wall_time_min,
        queue=queue,
        project=project,
        site_id=site.id,
        filter_tags={"workflow": f"{name}_{app_id}_{version}"},
        job_mode=job_mode
    )

def submit_all_jobs(num_nodes=1, wall_time_min = 60):

    site = Site.objects.get(site_name)

    # for start in range(begin_index, end_index, 128):
    for start in range(begin_index, end_index, 128):
        BatchJob.objects.create(
            num_nodes=num_nodes,
            wall_time_min=wall_time_min,
            queue=queue,
            project=project,
            site_id=site.id,
            filter_tags={"workflow": "MiniRun5_1E19_RHC_W_ION_Systematics_mlreco_v1_analysis_v1_v3"},
            # filter_tags={"job_start":f"{start}"},
            job_mode=job_mode
        )

if "flow2supera" in runs or "all" in runs:

    site = Site.objects.get(site_name)

    # parent_job_ids = [job.id for job in Job.objects.filter(
    #     site_id=site.id, 
    #     tags={"workflow": f"{name}_convert2h5_{version}"},
    #     )]

    #no parents for systematics
    parent_job_ids = []

    #GPU memory exceed error for larnd single run therefore node packing = 1
    for start in range(begin_index, end_index, spill_size):
        for i in range(start, start+spill_size):
            if i < end_index:
                create_single_dependent_job("flow2supera_v1", i, parent_job_ids, gpu_packing_count, start)

    print("flow2supera jobs created")

# if "submit_all_gpu" in runs:
#     # submit_all_jobs(num_nodes = spill_size//cpu_packing_count)
#     submit_all_jobs(num_nodes = min(spill_size, max_nodes), wall_time_min=360)

if "inference" in runs or "all" in runs:

    site = Site.objects.get(site_name)

    #node packing
    for start in range(begin_index, end_index, 128):
        for i in range(start, start+spill_size):
            if i < end_index:
                # parent_job_ids = [job.id for job in Job.objects.filter(
                # site_id=site.id, 
                # tags={"workflow": f"{name}_flow2supera_{version}", "index":f"{i}"},
                # )]
                parent_job_ids = []
                create_single_dependent_job("inference_v1", i, parent_job_ids, cpu_packing_count, start)

    print("inference jobs created")

if "analysis" in runs or "all" in runs:

    site = Site.objects.get(site_name)

    #node packing
    for start in range(begin_index, end_index, 128):
        for i in range(start, start+spill_size):
            if i < end_index:
                parent_job_ids = [job.id for job in Job.objects.filter(
                site_id=site.id, 
                tags={"workflow": f"{name}_inference_{version}", "index":f"{i}"},
                )]
                create_single_dependent_job("analysis_v1", i, parent_job_ids, cpu_packing_count, start)
            
    print("analysis jobs created")

#submit cpu jobs
if "submit_all_cpu" in runs:
    # submit_all_jobs(num_nodes = spill_size//cpu_packing_count)
    # submit_all_jobs(num_nodes = min(spill_size//cpu_packing_count,max_nodes), wall_time_min = 60)
    submit_all_jobs(num_nodes = num_nodes, wall_time_min = wall_time_min)





