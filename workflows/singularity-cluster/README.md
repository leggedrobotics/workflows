# Singularity Cluster Workflow:



## Overview:
- Isaac-gym container
## Singularity Workflow:

1. Install go ( [Instructions](https://sylabs.io/guides/3.0/user-guide/installation.html) )
2. Install singularity version 3.7.4 (current cluster singularity version, export correct version) ( [Instructions](https://sylabs.io/guides/3.0/user-guide/installation.html) )
3. Build the container (using `build.sh` script)
```
cd isaac_gym && python build.py
```

4. Convert docker container to singularity sif file
```
cd exports 
SINGULARITY_NOHTTPS=1 singularity build --sandbox isaac-gym.sif docker-daemon://rslethz/isaac-gym:latest
```

5. Start container on local machine and install additional dependencies
```
sudo singularity exec --nv --writable isaac-gym.sif bash
```

6. Tar folder without compression (is faster) and push to cluster
```
sudo tar -cvf isaac-gym-sif.tar isaac-gym.sif
scp isaac-gym-sif.tar jonfrey@euler:/cluster/work/rsl/jonfrey/learn_voxel_nav/containers
```

7. Schedule job with singularity resource in an interactive shell


```
bsub -n 16 -R singularity -R "rusage[mem=2096,ngpus_excl_p=1]" -W 04:00 -R "select[gpu_model0==GeForceRTX2080Ti]" -R "rusage[scratch=2000]" -R "select[gpu_driver>=470]" -Is bash
```

```
module load gcc/6.3.0 cuda/11.4.2
```

- Copy to local scratch of the node and unzip on the fly (This is the fastest method)
```
tar -xvf /cluster/work/rsl/jonfrey/learn_voxel_nav/containers/isaac-gym-sif.tar  -C $TMPDIR
```

- Start the singularity container
```
singularity exec -B $WORK/learn_voxel_nav:/home -B $HOME/isaac:/home/isaac --nv --writable --containall $TMPDIR/isaac-gym.sif bash -c "cd /home/legged_gym && python3 legged_gym/scripts/train.py --headless"

export ENV_WORKSTATION_NAME=euler && \
cd /home/isaac/legged_gym && \
python3 legged_gym/scripts/collect_traversability.py --headless --task=anymal_c_inital_poses --sim_device=cuda

```
Define `--containall` otherwise you will run into problems with possibly loaded modules on the cluster ! -->