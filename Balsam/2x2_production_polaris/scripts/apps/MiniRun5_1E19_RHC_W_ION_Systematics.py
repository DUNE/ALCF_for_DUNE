from balsam.api import ApplicationDefinition, BatchJob, Job, Site
import yaml

'''
MiniRun5 1E19 W_ION Systematics
'''

name = 'MiniRun5_1E19_RHC_W_ION_Systematics'
yaml_dir = f'../../specs/{name}/{name}'

site_name = "2x2_production_polaris"
path_2x2 = f"/grand/ALCF_for_DUNE/users/fathima/ALCF_for_DUNE/Balsam/{site_name}/data/2x2_sim"

"""
Functions
"""

def get_env_from_yaml(extension):
    yaml_file_path = f'{yaml_dir}{extension}'
    with open(yaml_file_path, 'r') as file:
        yaml_content = file.read()
    yaml_dict = yaml.safe_load(yaml_content)
    env = yaml_dict['base_envs'][0]['env']
    return env


"""
larnd
------------------------------------------
"""


extension = ".larnd.yaml"
env = get_env_from_yaml(extension)
app_id = "MiniRun5_Systematics_larnd"

class larnd(ApplicationDefinition):
    site = site_name
    print(env)
    environment_variables = env
    
    command_template = "./run_larnd_sim.sh"

    def shell_preamble(self):
        return f'''
        export ARCUBE_INDEX={self.job.data["i"]}
        module load singularity
        cd {path_2x2}/run-larnd-sim
        '''

larnd.sync()

"""
flow
------------------------------------------
"""


extension = ".flow.yaml"
env = get_env_from_yaml(extension)
app_id = "MiniRun5_Systematics_flow"

class flow(ApplicationDefinition):
    site = site_name
    print(env)
    environment_variables = env
    
    command_template = "./run_ndlar_flow.sh"

    def shell_preamble(self):
        return f'''
        export ARCUBE_INDEX={self.job.data["i"]}
        module load singularity
        cd {path_2x2}/run-ndlar-flow
        '''

flow.sync()

"""
plot
------------------------------------------
"""


extension = ".plots.yaml"
env = get_env_from_yaml(extension)
app_id = "MiniRun5_Systematics_plot"

class plot(ApplicationDefinition):
    site = site_name
    print(env)
    environment_variables = env
    
    command_template = "./run_validation.sh"

    def shell_preamble(self):
        return f'''
        export ARCUBE_INDEX={self.job.data["i"]}
        module load singularity
        cd {path_2x2}/run-validation
        '''

plot.sync()