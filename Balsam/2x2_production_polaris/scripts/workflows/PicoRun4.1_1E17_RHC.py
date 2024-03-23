from balsam.api import ApplicationDefinition, BatchJob, Job, Site
import yaml

#Machine variables
#########################
queue = "debug"         #
project="ALCF_for_DUNE" #
job_mode="mpi"          #
#########################

name = 'PicoRun4.1_1E17_RHC'
yaml_dir = f'../specs/{name}/{name}'
start = 0
single_size = 100
spill_size = 10 
site_name = "2x2_production_polaris"

runs = ["all","mid_submit"]

version = "v4"

"""
Functions
"""

def get_env_from_yaml(extension, idx):
    yaml_file_path = f'{yaml_dir}{extension}'
    with open(yaml_file_path, 'r') as file:
        yaml_content = file.read()
    yaml_dict = yaml.safe_load(yaml_content)
    env = yaml_dict['base_envs'][idx]['env']
    return env

def create_jobs(app_id, size, node_packing_count):

    for i in range(size):
        Job.objects.create( app_id=app_id,
                            site_name=site_name,
                            workdir=f"workdir/{i}_{app_id}",
                            node_packing_count=node_packing_count,
                            tags={"workflow": f"{name}_{app_id}_{version}"},
                            data={"i": i})

def create_single_dependent_job(app_id, i, parent_ids, node_packing_count):

    Job.objects.create( app_id=app_id,
                        site_name=site_name,
                        workdir=f"workdir/{i}_{app_id}",
                        node_packing_count=node_packing_count,
                        tags={"workflow": f"{name}_{app_id}_{version}"},
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

if "edepsim_nu" in runs or "all" in runs:
    create_jobs(app_id, single_size, single_size)
    submit_filtered_jobs(app_id)

if "edepsim_rock" in runs or "all" in runs:
    create_jobs(app_id, single_size, single_size)
    submit_filtered_jobs(app_id)

if "hadd_nu" in runs or "all" in runs:

    site = Site.objects.get(site_name)

    parent_job_ids = [job.id for job in Job.objects.filter(
        site_id=site.id, 
        tags={"workflow": f"{name}_edep_sim_nu_{version}"},
        )]

    for i in range(spill_size):
        create_single_dependent_job(app_id, i, parent_job_ids, spill_size)
    
    # submit_filtered_jobs(app_id)

if "mid_submit" in runs:
    submit_filtered_jobs(app_id)

if "hadd_rock" in runs or "all" in runs:

    site = Site.objects.get(site_name)

    parent_job_ids = [job.id for job in Job.objects.filter(
        site_id=site.id, 
        tags={"workflow": f"{name}_edep_sim_rock_{version}"}
        )]

    for i in range(spill_size):
        create_single_dependent_job(app_id, i, parent_job_ids, spill_size)
    
    # submit_filtered_jobs(app_id)
if "mid_submit" in runs:
    submit_filtered_jobs(app_id)

if "spill" in runs or "all" in runs:

    site = Site.objects.get(site_name)

    parent_job_ids = [job.id for job in Job.objects.filter(
        site_id=site.id, 
        tags={"workflow": f"{name}_hadd_nu_{version}"},
        )]+[job.id for job in Job.objects.filter(
        site_id=site.id, 
        tags={"workflow": f"{name}_hadd_rock_{version}"},
        )]

    for i in range(spill_size):
        create_single_dependent_job(app_id, i, parent_job_ids, spill_size)

    # submit_filtered_jobs(app_id)
if "mid_submit" in runs:
    submit_filtered_jobs(app_id)

if "convert2h5" in runs or "all" in runs:

    site = Site.objects.get(site_name)

    parent_job_ids = [job.id for job in Job.objects.filter(
        site_id=site.id, 
        tags={"workflow": f"{name}_spill_{version}"},
        )]

    for i in range(spill_size):
        create_single_dependent_job(app_id, i, parent_job_ids, spill_size)

    # submit_filtered_jobs(app_id)

if "mid_submit" in runs:
    submit_filtered_jobs(app_id)

if "larnd" in runs or "all" in runs:

    site = Site.objects.get(site_name)

    parent_job_ids = [job.id for job in Job.objects.filter(
        site_id=site.id, 
        tags={"workflow": f"{name}_convert2h5_{version}"},
        )]

    for i in range(spill_size):
        create_single_dependent_job(app_id, i, parent_job_ids, 1)

    # submit_filtered_jobs(app_id)
if "mid_submit" in runs:
    submit_filtered_jobs(app_id)

if "flow" in runs or "all" in runs:

    site = Site.objects.get(site_name)

    parent_job_ids = [job.id for job in Job.objects.filter(
        site_id=site.id, 
        tags={"workflow": f"{name}_larnd_{version}"},
        )]

    for i in range(spill_size):
        create_single_dependent_job(app_id, i, parent_job_ids, spill_size)

    # submit_filtered_jobs(app_id)

if "mid_submit" in runs:
    submit_filtered_jobs(app_id)

if "submit_all" in runs:
    submit_all_jobs()





