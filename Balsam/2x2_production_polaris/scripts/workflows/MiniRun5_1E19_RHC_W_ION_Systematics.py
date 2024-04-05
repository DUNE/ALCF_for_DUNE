from balsam.api import ApplicationDefinition, BatchJob, Job, Site
import yaml

#Machine variables
#########################
queue = "prod"          #
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
#need to experiment with this as we have 1024 jobs
gpu_packing_count = 1

if queue == "debug":
    cpu_packing_count = 16

max_nodes = 32
name = 'MiniRun5_1E19_RHC_W_ION_Systematics'

start = 272
spill_size = 128

# start = 16
# spill_size = 128

site_name = "2x2_production_polaris"

runs = ["all","submit_all_gpu","submit_all_cpu"]

version = "v0"

"""
Functions
"""

def create_jobs(app_id, size, node_packing_count):

    for i in range(size):
        Job.objects.create( app_id=app_id,
                            site_name=site_name,
                            workdir=f"workdir/{i}_{app_id}",
                            node_packing_count=node_packing_count,
                            tags={"workflow": f"{name}_{app_id}_{version}", "index":f"{i}"},
                            data={"i": i})

def create_single_dependent_job(app_id, i, parent_ids, node_packing_count):

    Job.objects.create( app_id=app_id,
                        site_name=site_name,
                        workdir=f"workdir/{i}_{app_id}",
                        node_packing_count=node_packing_count,
                        tags={"workflow": f"{name}_{app_id}_{version}", "index":f"{i}"},
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

    BatchJob.objects.create(
        num_nodes=num_nodes,
        wall_time_min=wall_time_min,
        queue=queue,
        project=project,
        site_id=site.id,
        job_mode=job_mode
    )

if "larnd" in runs or "all" in runs:

    site = Site.objects.get(site_name)

    # parent_job_ids = [job.id for job in Job.objects.filter(
    #     site_id=site.id, 
    #     tags={"workflow": f"{name}_convert2h5_{version}"},
    #     )]

    #no parents for systematics
    parent_job_ids = []

    #GPU memory exceed error for larnd single run therefore node packing = 1
    for i in range(start,start+spill_size):
        create_single_dependent_job("larnd", i, parent_job_ids, gpu_packing_count)

    print("larnd jobs created")

# if "submit_all_gpu" in runs:
#     # submit_all_jobs(num_nodes = spill_size//cpu_packing_count)
#     submit_all_jobs(num_nodes = min(spill_size, max_nodes), wall_time_min=360)

if "flow" in runs or "all" in runs:

    site = Site.objects.get(site_name)

    #node packing
    for i in range(start,start+spill_size):
        parent_job_ids = [job.id for job in Job.objects.filter(
        site_id=site.id, 
        tags={"workflow": f"{name}_larnd_{version}", "index":f"{i}"},
        )]
        create_single_dependent_job("flow", i, parent_job_ids, cpu_packing_count)

    print("flow jobs created")

if "plot" in runs or "all" in runs:

    site = Site.objects.get(site_name)

    #node packing
    for i in range(start,start+spill_size):
        parent_job_ids = [job.id for job in Job.objects.filter(
        site_id=site.id, 
        tags={"workflow": f"{name}_flow_{version}", "index":f"{i}"},
        )]
        create_single_dependent_job("plot", i, parent_job_ids, cpu_packing_count)
    
    print("Plot jobs created")

#submit cpu jobs
if "submit_all_cpu" in runs:
    # submit_all_jobs(num_nodes = spill_size//cpu_packing_count)
    # submit_all_jobs(num_nodes = min(spill_size//cpu_packing_count,max_nodes), wall_time_min = 60)
    submit_all_jobs(num_nodes = 128, wall_time_min = 60)





