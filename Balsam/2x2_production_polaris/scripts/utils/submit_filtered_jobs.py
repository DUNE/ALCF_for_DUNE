site_name = "2x2_production_polaris"
name = "MiniRun5_1E19_RHC_W_ION_Systematics"
app_id = "flow"
version = "v0"
queue= "prod"
project = "ALCF_for_DUNE"


from balsam.api import Job, BatchJob, Site

def submit_filtered_jobs(app_id, num_nodes=128, wall_time_min = 30):

    site = Site.objects.get(site_name)

    BatchJob.objects.create(
        num_nodes=num_nodes,
        wall_time_min=wall_time_min,
        queue=queue,
        project=project,
        site_id=site.id,
        filter_tags={"workflow": "MiniRun5_1E19_RHC_W_ION_Systematics_plot_v0","job_start":"16"},
        job_mode="mpi"
    )

submit_filtered_jobs(app_id)