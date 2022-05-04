#  Getting Started - Python for Learning

# Prephase

## What it is: 
This repository gives an example implementation of a deep learning project.   
We try to apply to the best practices recommended for python.  
Additionally, we integrate examples for logging, visualization, configuration loading, and hyperparameter search.

## What it is not: 
This repository is not an example on how to train your semantic segmentation network.  
It illustrates a fully minimalistic implementation. 
The choosen hyperparameter for training the network and data augmentation are arbitrarily.  

## Table of Contents
- [Getting Started - Python for Learning](#getting-started---python-for-learning)
- [Prephase](#prephase)
  - [What it is:](#what-it-is)
  - [What it is not:](#what-it-is-not)
  - [Table of Contents](#table-of-contents)
- [Paper and Video](#paper-and-video)
- [Installation](#installation)
    - [Setting up NeptuneAI:](#setting-up-neptuneai)
    - [Define your Environment Name:](#define-your-environment-name)
    - [Define your Environment Variables:](#define-your-environment-variables)
    - [Downloading Example Dataset:](#downloading-example-dataset)
- [TODO:](#todo)
# Paper and Video

It`s best practice to include the citation of your paper in your GitHub repository. 

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
- opencv-python 4.5.5.62
- neptune-client 0.14.0
- matplotlib
- numpy 1.22.3 
- imageio
- pillow 9.1.0
- scikit-image 0.19.1
- torchvision 0.11.2
- pyyaml 6.0
- pytorch-lightning 1.5.7
- pytorch 1.10.1

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

# TODO:
- Add eval and optuna hyperparameter search.
- Add some helper scripts to deploy on the cluster 
- Correct comments
- Providing VSCode files
- Code formatting
- GitHub Actions
- Conda Environment
- PyTest full coverage