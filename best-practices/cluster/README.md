# Official documentation:
Read this at first very carefull:
https://scicomp.ethz.ch/wiki/Getting_started_with_clusters

Available software packages pre-installed
https://scicomp.ethz.ch/wiki/Euler_applications_and_libraries

# Dont`s:
- ![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+) Only log into the cluster using a terminal.  
    Do not use VSCode otherwise your account will be banned. 
- ![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+) Schedule experiments only if you are sure your code runs.
- ![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+) Make sure to not loss experiment outputs.
- ![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+) When searching for hyperparameters don`t do a lazy grid-search (be smart. alter one of the hyperparameters after an other)
- ![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+) Only reserve the resources you need. Cores, Memory, Time, GPUs.
- ![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+) Using more resources for a single run is often worse than running 2 jobs with half the resources (% of code fully parallizable).
# Data management:
First read the data management in the cluster documentation.


## Summary:
- `/cluster/home`:  
Home Directory is 16GB.  
Store your code / GitHub repositories here and conda environment for python.  
Can be transferred extremely fast to the compute nodes.  

- `/cluster/scratch`: 
Temporary directory for 2 Weeks with 2TB.  
If a lot of small files need to be transferred to the compute node this may be extremely slow.  
Use for datasets or maybe your experiment results. RULES `cat $SCRATCH/__USAGE_RULES__`  

- `/work/usergroup`: 
Same as local scratch but persistent.   
Use for datasets or maybe your experiment results.  


- `$TMPDIR`: Local scratch (on each compute node).  
Needs to be reserved when submitting a job with `bsub`.   
Provides SSD storage on the compute node itself.  
Is extremely fast especially for a lot of file access (Not penetrating the cluster network).  
Therefore good for everything you need to often read and write.  
Example ImageNet dataset with individual .pngs. Transfer to local scratch before starting the training.  

![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+) **WARNING**: All directories have file limits aswell!  
It`s preferable to transfer 1 big tarred file than a lot of individual small files. 

## Transfering data fast:
## Copy data:
- [scp](https://linux.die.net/man/1/scp) 
```bash
scp -r /home/username/Documents username@euler.ethz.ch:/cluster/home/username
```
Transfers all contents (`-r`) of your local machine Documents folder to your home directory on the cluster.

- [rsync](https://linux.die.net/man/1/rsync)
```bash
rsync -r -v --delete --exclude 'something/*' --exclude '__pycache__' --exclude '*.pyc' --exclude '*.ipynb' /home/username/Documents jonfrey@euler:/cluster/home/jonfrey/project
```
Syncs all (`-r`) files in your Documents folder to your `home/project` directory on the cluster.  
Deletes everything within your cluster `home/project` directory to match your Documents folder (`--delete`, be carefull to not delete important things on the cluster!). 
Ignores everything in the `/home/username/Documents/something` folder and specific file endings. 

# Modules:
Available software packages pre-installed
https://scicomp.ethz.ch/wiki/Euler_applications_and_libraries

Modules to use for python with GPU support:
```bash
module load gcc/6.3.0 cuda/11.3.1 cudnn/8.0.5 python_gpu/3.8.5
```

ETH Proxy activate in the actual compute node (not the login node):
```bash
module load eth_proxy
```

See active modules:
```
module list
```

See available modules:
```
module avail
```

# Scheduling:
- Number of CPUs
- Memory
- Scratch Memory
- GPUs
- Driver
- Group
- Debugging, Interactive

# Tipps:
Update bashrc for colors
Using debugging with tmux
Checking RAM and CPU usage of a Job in hindsight
Using the Proxy
Installing Conda

Python Workflow Options:
1. Cluster Python Module
2. Conda Enviornment
3. Singularity Container






