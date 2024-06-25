from balsam.api import ApplicationDefinition, BatchJob, Job, Site
import yaml

'''
MiniRun5 1E19 W_ION Systematics MLReco v1
'''

#added later

name = 'MiniRun5_1E19_RHC_W_ION_Systematics_mlreco_v1'
yaml_dir = f'../../specs/{name}/{name}'

site_name = "2x2_production_polaris"
path_2x2 = f"/home/fathimamaha/{site_name}/data/2x2_sim"

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


extension = ".flow2supera.yaml"
env = get_env_from_yaml(extension)

class flow2supera_v1(ApplicationDefinition):
    site = site_name
    print(env)
    environment_variables = env
    
    command_template = "./run_flow2supera.sh"

    def shell_preamble(self):
        return f'''
        export ARCUBE_INDEX={self.job.data["i"]}
        module use /soft/modulefiles
        module load spack-pe-base
        module load apptainer
        cd {path_2x2}/run-mlreco
        '''

flow2supera_v1.sync()


extension = ".inference.yaml"
env = get_env_from_yaml(extension)

class inference_v1(ApplicationDefinition):
    site = site_name
    print(env)
    environment_variables = env
    
    command_template = "./run_mlreco_inference.sh"

    def shell_preamble(self):
        return f'''
        export ARCUBE_INDEX={self.job.data["i"]}
        module use /soft/modulefiles
        module load spack-pe-base
        module load apptainer
        cd {path_2x2}/run-mlreco
        '''

inference_v1.sync()


extension = ".analysis.yaml"
env = get_env_from_yaml(extension)
app_id = "MiniRun5_Systematics_mlreco_analysis"

class analysis_v1(ApplicationDefinition):
    site = site_name
    print(env)
    environment_variables = env
    
    command_template = "./run_mlreco_analysis.sh"

    def shell_preamble(self):
        return f'''
        export ARCUBE_INDEX={self.job.data["i"]}
        module use /soft/modulefiles
        module load spack-pe-base
        module load apptainer
        cd {path_2x2}/run-mlreco
        '''

analysis_v1.sync()