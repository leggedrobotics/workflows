# Using Python on the Cluster

## Option 1: Default Cluster Python
The cluster already provides a wide range of python versions with a set of pre-installed packages. [link](https://scicomp.ethz.ch/wiki/Python_on_Euler)  
You can use `pip` to install the missing packages. 
Follow the documentation here [link](https://scicomp.ethz.ch/wiki/Python)

### Loading the desired python modules
```shell
module load python_gpu/3.8.5 gcc/8.2.0
which python
```
Returns `/cluster/apps/nss/gcc-8.2.0/python/3.8.5/x86_64/bin/python` depending on the requested python and gcc version.


### Usacase

- ![#8fce00](https://via.placeholder.com/15/8fce00/000000?text=+) Minimal setup effort
- ![#8fce00](https://via.placeholder.com/15/8fce00/000000?text=+) No specific requirments on package or python version
 - ![#8fce00](https://via.placeholder.com/15/8fce00/000000?text=+) Some packages are optimized for the cluster hardware 
- ![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+) No full control over the python version and installed packages (If desired use Option 2 or Option 3)  


## Option 2: Miniconda Installation

Use anaconda to set up a custom python environment ([link](https://docs.conda.io/en/latest/miniconda.html)).

```shell
cd $HOME
wget https://repo.anaconda.com/miniconda/Miniconda3-py38_4.9.2-Linux-x86_64.sh
chmod +x ./Miniconda3-py38_4.9.2-Linux-x86_64.sh
./Miniconda3-py38_4.9.2-Linux-x86_64.sh
```

- ![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+) [WARNING] Install Miniconda in your `$HOME` directory. This installation consists of a lot of small files. Using any other directory leads to undesirable loading times of the python environment, or loading packages takes a significant amount of time. Remember your `$HOME` is copied to your local execution node extremely fast.

### Usacase

- ![#8fce00](https://via.placeholder.com/15/8fce00/000000?text=+) Multiple python environments

- ![#8fce00](https://via.placeholder.com/15/8fce00/000000?text=+) Specific each package and conda version
 
- ![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+) Takes up significant storage of your `$HOME` directory. If you want to install many big libraries like TensorFlow and PyTorch the `$HOME/.miniconda` folder can be quite big.  


## Option 3: Singularity
Run everything inside a singularity container.  
For this follow the [Singularity-Cluster](./workflows/singularity-cluster) guide.

### Usacase
- ![#8fce00](https://via.placeholder.com/15/8fce00/000000?text=+) If special packages or dependencies need to be installed that are not available with `pip` or you need `sudo`-rights to install them. 
- ![#8fce00](https://via.placeholder.com/15/8fce00/000000?text=+) Works well if you know all your dependencies and you don't have to change anything.
- ![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+) Quite a lot of work to change a package version. 