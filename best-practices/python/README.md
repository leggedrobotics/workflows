# Best Practices Python
## Coding Style
Set a coding style for your project:
https://google.github.io/styleguide/pyguide.html

## Code Formatting
Use a code formatter!
We use black formatter for formatting the python code and flake8 for linting. To run the formatter:

```shell
# for formatting
pip3 install black
black --line-length 120 .
```

Get where black is installed:
```shell
python3 -c 'import black; from pathlib import Path; print(Path(black.__file__).parent)'
```

In VSCode `CTRL`+`Shift`+`P` edit your `settings.json`:
```json  
    "editor.formatOnSave": true,
    "python.formatting.blackPath": "~/.local/lib/python3.8/site-packages/black",
``` 


## Code Linting
```shell
# for checking lints
pip install flake8
flake8 .
```

In VSCode `CTRL`+`Shift`+`P` edit your `settings.json`:
```json
    "python.linting.flake8Enabled": true,
    "python.linting.flake8Args": [
        "--ignore=E402,E501,W503",
        "--extend-ignore=E203",
        "--exclude=*__init__.py,_*,.vscode,.git",
        "--max-complexity=18",
        "--max-line-length=120",
    ],
```

Alternativly for settings you can provide the template `.flake8` configuration file.


## Usefulls Tools

### Logging 
For all ML-projects we highly recommend to use a logging framework.  
We suggest you to user either [NeptuneAI](https://neptune.ai/) or [Weights & Biases](https://wandb.ai/site).   
They are straight forward to integrate.  
On the cluster make sure to activate the proxy module.  


****### Debugging
VSCode Debugger is great

### Virtual Environments

| **Tool**            | **Pros**                                                                             | **Cons**                                                                      |
| ------------------- | ------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------- |
| System Installation | +simple<br> +works with ROS                                                          | -cannot be shared<br> -dependecies problems when working on multiple projects |
| Conda               | + easy to setup and share<br> + wide adopted<br> + clear separation between projects | +works only with ROS with additional packages                                 |
| Virual Env          |                                                                                      |                                                                               |

## PyTorch
`PytorchLightning`
Pros:
- Great for all supervised learning tasks
- Great if problem formulated in Training, Validation, Test datasets
- Multi-GPU
- 16 Bit support
- Reduces boiler plate code

Cons:
- For certain special cases restircts you

## Configuration Files





