## Running 2x2_sim on ALCF Polaris

Dated: 2 Aug 2024 (Depending upon the machine software updates, some instructions might be obsolete later)

File modifications:
- Replacing loading singularity:   
  Old:
  ```
  module load singularity
  ```
  New:
  ```
  module use /soft/modulefiles
  module load spack-pe-base
  module load apptainer
  ```
- Replacing loading Python   
  Old:
  ```
  module load python/3.11
  ```
  New:
  ```
  module use /soft/modulefiles
  module load conda
  conda activate
  ```
-Replacing loading Cuda    
  Old:
  ```
  module load cudatoolkit/11.7
  ```
  New:
  ```
  module load cudatoolkit-standalone/11.8.0
  ```
- Changes to loading singularity    
  In the file `util/reload_in_container.inc.sh`, make the container aware of external folders
  Old:
  ```
  singularity exec -B $ARCUBE_DIR $ARCUBE_CONTAINER_DIR/$ARCUBE_CONTAINER /bin/bash "$0" "$@"
  ```
  New:
  ```
  singularity exec --nv -B $ARCUBE_DIR,/grand/ALCF_for_DUNE/users/fathima,$CVMFS_HOME_DIRECTORY:/cvmfs,/opt/nvidia/hpc_sdk/Linux_x86_64/23.9:/opt/cuda $ARCUBE_CONTAINER_DIR/$ARCUBE_CONTAINER /bin/bash "$0" "$@"
  ```




