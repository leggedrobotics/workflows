# Official documentation:
Read this at first very carefull:
https://scicomp.ethz.ch/wiki/Getting_started_with_clusters

Available software packages pre-installed
https://scicomp.ethz.ch/wiki/Euler_applications_and_libraries

# Dont`s:
- ![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+) Only log into the cluster using a terminal.  
    Do not use VSCode otherwise your account will be banned. 
- ![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+) Schedule experiments only if you are sure your code runs.
- ![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+) Make sure that all jobs jo schedule can be analyzed and outputs are saved correctly.
- ![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+) When searching for hyperparameters don`t do a lazy grid-search (be smart. alter one of the hyperparameters after another)
- ![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+) Only reserve the resources you need. Cores, Memory, Time, GPUs.
- ![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+) Using more resources for a single run is often worse than running 2 jobs with half the resources (% of code fully parallizable).
# Data management:
First read the data management in the cluster documentation.


## Summary:
- `/cluster/home`:  
Home Directory is 16GB.  
Store your code / GitHub repositories here and conda environment for python.  
Can be transferred extremely fast to the compute nodes. 
Even for a lot of small files the speed is not reduced based on the number of copied files.

- `/cluster/scratch`: 
Temporary directory for 2 Weeks with 2TB.  
If a lot of small files need to be transferred to the compute node this may be extremely slow.
A file limit automatically triggers a massive reduction in transmission speed. 
This is due to the storage is connected via a network which can slow down the full cluster.  
Used for datasets or maybe your experiment results. RULES `cat $SCRATCH/__USAGE_RULES__`  

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

## Transfering data to local compute node:
Tar all data within a folder without compression:
It`s recommended to perform the tar process on your local machine and then transfer the .tar to the cluster.
```
tar -cvf $HOME/some_folder.tar $HOME/some_folder
```
When you submit your run script copy and extract the data to the local SSD on the compute node: 
```
tar -xvf $HOME/some_folder.sif  -C $TMPDIR
```


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

Example command:
```
bsub -n 18  \
    -W 4:00 \
    -R singularity  \
    -R "rusage[mem=3096,ngpus_excl_p=1]" \
    -o $HOME/results.out \
    -R "select[gpu_mtotal0>=10000]" \
    -R "rusage[scratch=2000]" \
    -R "select[gpu_driver>=470]" \
    $HOME/some_script.sh 
```
- `n` Number of CPU-Cores
- `mem=3096` Memory in MB per Cores
- `-R "rusage[scratch=2000]"` Scratch Memory in MB per Core on local SSD
- `ngpus_excl_p=1` Use a single GPU
- `-R "select[gpu_driver>=470]" ` GPU Driver Version
- `-R "select[gpu_mtotal0>=10000]"` GPU Memory over 10000MB
- `-o $HOME/results.out` File to store the consol output
- `-I` Get an interactive job
- `-s` Will give you a login shell to the compute node
# Tipps:
### Checking your usergroup: 
```
my_share_info
```

### Check file limits and memory limits of different directories
```
lquota $HOME
```

### Interactive Debugging:

To debug on the cluster and get your code running without scheduling for each trial a new job you can get a shell on at execution node:
```
bsub -Is ..specify other resources for the job.. bash
```
Using [tmux](https://tmuxcheatsheet.com/) is even more convenient allows you to have multiple terminal windows on the same compute node. 
```
module load tmux
bsub -Is ..specify other resources for the job.. tmux
```

### Colors on the cluster:
Append to following to your `$HOME/.bashrc` on the cluster to get color support. 
```
if [ -n "$force_color_prompt" ]; then
    if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
        # We have color support; assume it's compliant with Ecma-48
        # (ISO/IEC-6429). (Lack of such support is extremely rare, and such
        # a case would tend to support setf rather than setaf.)
        color_prompt=yes
    else
        color_prompt=
    fi
fi

if [ "$color_prompt" = yes ]; then
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
else
    PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
fi
unset color_prompt force_color_prompt
```

### Monitor resource usage:
Prints all running or scheduled jobs:
```
bjobs
```


Provides detailed information about a job.  
If you have a low `Resource usage` change your core usage or write more performant code.
```
bbjobs JOB_ID
```

### Shareholder information:
```
my_share_info
```
