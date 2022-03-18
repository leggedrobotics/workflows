# Singularity Cluster:

## Assumptions:
- We assume you have Docker installed and know what you are doing.  
- The overall workflow is to create a Docker container that fits your purposes.  
- We convert the Docker container into a singularity container on your local machine.  
- We push the container to the cluster and execute it on the cluster.  

## Workflow

### 1. Install go on your local machine ( [Instructions](https://sylabs.io/guides/3.0/user-guide/installation.html) )
### 2. Install singularity version 3.7.4 (current cluster singularity version, export correct version) ( [Instructions](https://sylabs.io/guides/3.0/user-guide/installation.html) )
### 3. Create your docker container that meets your purposes.  
- You will most likely create a Dockerfile based on the Nvidia Docker container with GPU support.
- Follow the installation guide here if you want to use the Nvidia Docker ( [Instructions](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html) )  
- Here you can find all DockHub Images available ([Instructions](https://hub.docker.com/r/nvidia/cuda/tags?page=1&ordering=last_updated))    
- Then build your container using docker and give it a tag.  
- Run the container and make sure everything works on your local machine.


### 4. Convert docker container to singularity sif file
```
cd exports 
SINGULARITY_NOHTTPS=1 singularity build --sandbox your-container-tagname.sif docker-daemon://your-container-tagname:latest
```

### 5. Start container on local machine and install additional dependencies
```
sudo singularity exec --nv --writable your-container-tagname.sif bash
```

### 6. Tar folder without compression (is faster) and push to cluster (Choose cluster locating depending on if this should be permanent storage)
```
sudo tar -cvf your-container-tagname.tar your-container-tagname.sif
scp your-container-tagname.tar jonfrey@euler:/cluster/work/rsl/your_usernamer/containers
```

### 7. Schedule job with singularity resource in an interactive shell

```
bsub -n 16 -R singularity -R "rusage[mem=2096,ngpus_excl_p=1]" -W 04:00 -R "select[gpu_model0==GeForceRTX2080Ti]" -R "rusage[scratch=2000]" -R "select[gpu_driver>=470]" -Is bash
```

```
module load gcc/6.3.0 cuda/11.4.2
```

- Copy to local scratch of the node and unzip on the fly (This is the fastest method)
```
tar -xvf /cluster/work/rsl/your_usernamer/containers/your-container-tagname.tar  -C $TMPDIR
```

- Start the singularity container
```
singularity exec -B $WORK:/home --nv --writable --containall $TMPDIR/your-container-tagname.sif bash -c "runscript.sh"
```
Define `--containall` otherwise you will run into problems with possibly loaded modules on the cluster!