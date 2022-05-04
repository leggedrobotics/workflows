#  README


# Documentation
This repository gives an example implementation of a deep learning project.   
We try to apply to the best practices recommended for python.  
Additionally, we integrate examples for logging, visualization, configuration loading, and hyperparameter search.

## TODO:
- Make the Cityscapes training run with the normal amount of classes (modify the network).
- Check correct visualization.
- Add eval and optuna hyperparameter search.
- Add some helper scripts to deploy on the cluster 



## Table of Contents
- [README](#readme)
- [Documentation](#documentation)
  - [TODO:](#todo)
  - [Table of Contents](#table-of-contents)
- [Paper and Video](#paper-and-video)
- [Installation](#installation)
    - [Setting up NeptuneAI:](#setting-up-neptuneai)
    - [Define your Environment Name:](#define-your-environment-name)
    - [Define your Environment Variables:](#define-your-environment-variables)
    - [Downloading Example Dataset:](#downloading-example-dataset)
# Paper and Video
This work is currently under review.

Jonas Frey, ...., .... , **Your Paper Title**”, in *IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)*, 2022.

```latex
@inproceedings{frey2022traversability,
  author={Jonas Frey},
  journal={under review: IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)},
  title={Your Paper Title},
  year={2022}
}
```
# Installation
The code was tested on:  
`Ubuntu 20.04`, `Nvidia Driver Version: 470.82.01`, `CUDA Version: 11.4 and 11.3`, `GPUs: GTX1080TI and RTX3090 and RTX2080TI`   

Install [PyTorch](https://pytorch.org/get-started/): 
```
pip3 install torch==1.10.2+cu113 torchvision==0.11.3+cu113 torchaudio==0.10.2+cu113 -f https://download.pytorch.org/whl/cu113/torch_stable.html
```

Install the project:
```
pip3 install -e ./template_project_name
```

Project Dependencies (automatically installed): 
- Pytorch Lighting
- OpenCV
- Neptune-Client
- Pillow
- Matplotlib

### Setting up NeptuneAI:
Append your `NEPTUNE_API_TOKEN` to your `~/.bashrc` at the bottom:
```
export NEPTUNE_API_TOKEN="something"
```
### Define your Environment Name:
The global variable `$ENV_WORKSTATION_NAME` is used to load the correct configuration file, which should include all global paths which are system dependent. 

Append to your `~/.bashrc` at the bottom:
```
export ENV_WORKSTATION_NAME="some_name"
```

### Define your Environment Variables:
Create an environment configuration file `cfg/env/some_name.yml`:
```
results: results
cityscapes_root: /cluster/work/rsl/Cityscapes
```
Current demo-version only expects the global path to the Cityscapes dataset and the results directory.  
All paths can be either provided relative to this repository or as global paths.  

The current experiments logging output will be stored in the folder `template_project_name/results/`.



### Downloading Example Dataset:
Ask for the GoogleDrive link to Download the Cityscapes dataset fork or download directly from https://www.cityscapes-dataset.com/  
Expected Folder Structure:
```
..\Cityscapes
        \gtCoarse
        \gtFine
        \gitFine_trainvaltest
        \leftImg8but
```
