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
path_2x2 = f"/grand/ALCF_for_DUNE/users/fathima/ALCF_for_DUNE/Balsam/{site_name}/data/2x2_sim"

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


"""
nu - edepsim
------------------------------------------
"""

extension = ".nu.yaml"
env = get_env_from_yaml(extension, 0)
app_id = "edep_sim_nu"

class edep_sim_nu(ApplicationDefinition):
    site = site_name
    print(env)
    environment_variables = env
    
    command_template = "./run_edep_sim.sh"

    def shell_preamble(self):
        return f'''
        export ARCUBE_INDEX={self.job.data["i"]}
        module load singularity
        cd {path_2x2}/run-edep-sim
        '''

edep_sim_nu.sync()


"""
rock-edepsim
------------------------------------------
"""

extension = ".rock.yaml"
env = get_env_from_yaml(extension, 0)
app_id = "edep_sim_rock"

class edep_sim_rock(ApplicationDefinition):
    site = site_name
    print(env)
    environment_variables = env
    
    command_template = "./run_edep_sim.sh"

    def shell_preamble(self):
        return f'''
        export ARCUBE_INDEX={self.job.data["i"]}
        module load singularity
        cd {path_2x2}/run-edep-sim
        '''

edep_sim_rock.sync()

"""
nu-hadd
------------------------------------------
"""


extension = ".hadd.yaml"
env = get_env_from_yaml(extension, 0)
app_id = "hadd_nu"

class hadd_nu(ApplicationDefinition):
    site = site_name
    print(env)
    environment_variables = env
    
    command_template = "./run_hadd.sh"

    def shell_preamble(self):
        return f'''
        export ARCUBE_INDEX={self.job.data["i"]}
        module load singularity
        cd {path_2x2}/run-hadd
        '''

hadd_nu.sync()


"""
rock-hadd
------------------------------------------
"""

extension = ".hadd.yaml"
env = get_env_from_yaml(extension, 1)
app_id = "hadd_rock"

class hadd_rock(ApplicationDefinition):
    site = site_name
    print(env)
    environment_variables = env
    
    command_template = "./run_hadd.sh"

    def shell_preamble(self):
        return f'''
        export ARCUBE_INDEX={self.job.data["i"]}
        module load singularity
        cd {path_2x2}/run-hadd
        '''

hadd_rock.sync()

"""
------------------------------------------
"""

"""
spill-build
------------------------------------------
"""
# scripts/fwsub.py --runner SimFor2x2_v3_LArND --base-env "$name".larnd --name "$name".larnd --size $spill_size --start $start
# scripts/fwsub.py --runner SimFor2x2_v3_Flow --base-env "$name".flow --size $spill_size --start $start
# scripts/fwsub.py --runner SimFor2x2_v3_Plots --base-env "$name".plots --size $spill_size --start $start

extension = ".spill.yaml"
env = get_env_from_yaml(extension, 0)
app_id = "spill"

class spill(ApplicationDefinition):
    site = site_name
    print(env)
    environment_variables = env
    
    command_template = "./run_spill_build.sh"

    def shell_preamble(self):
        return f'''
        export ARCUBE_INDEX={self.job.data["i"]}
        module load singularity
        cd {path_2x2}/run-spill-build
        '''

spill.sync()

"""
convert2h5
------------------------------------------
"""


extension = ".convert2h5.yaml"
env = get_env_from_yaml(extension, 0)
app_id = "convert2h5"

class convert2h5(ApplicationDefinition):
    site = site_name
    print(env)
    environment_variables = env
    
    command_template = "./run_convert2h5.sh"

    def shell_preamble(self):
        return f'''
        export ARCUBE_INDEX={self.job.data["i"]}
        module load singularity
        cd {path_2x2}/run-convert2h5
        '''

convert2h5.sync()

"""
larnd
------------------------------------------
"""


extension = ".larnd.yaml"
env = get_env_from_yaml(extension, 0)
app_id = "larnd"

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
env = get_env_from_yaml(extension, 0)
app_id = "flow"

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


extension = ".plot.yaml"
env = get_env_from_yaml(extension, 0)
app_id = "plot"

class plot(ApplicationDefinition):
    site = site_name
    print(env)
    environment_variables = env
    
    command_template = "./run_validation.sh"

    def shell_preamble(self):
        return f'''
        export ARCUBE_INDEX={self.job.data["i"]}
        module load singularity
        cd {path_2x2}/validation
        '''

plot.sync()