#  README

Training a sparse 3D neural network to estimate traversability for a legged robot based on a 3D occupancy map
![](docs/natural_env.jpg)

# Documentation
This repository includes the terrain generation and sparse 3D neural network learning code.  
The traversability collection code will be open sourced in the near furture.  
The ROS code is available here: [https://github.com/leggedrobotics/lvn_utils](https://github.com/leggedrobotics/lvn_utils)  
## Table of Contents
- [README](#readme)
- [Documentation](#documentation)
  - [Table of Contents](#table-of-contents)
- [Paper and Video](#paper-and-video)
- [Performance](#performance)
- [Installation](#installation)
# Paper and Video
This work is currently under review.

Jonas Frey, David Hoeller, Shehryar Khattak, Marco Hutter, “**Locomotion Policy Guided Traversability Learning using Volumetric
Representations of Complex Environments**”, in *IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)*, 2022.

```latex
@inproceedings{frey2022traversability,
  author={Frey, Jonas and Hoeller, David and Khattak, Shehryar and Marco, Hutter},
  journal={under review: IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)},
  title={Locomotion Policy Guided Traversability Learning using Volumetric
Representations of Complex Environments},
  year={2022}
}
```
# Performance

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

Setting up NeptuneAI

Setting Identifier for Global Configuration File

Downloading Example Dataset
