# Best Practices Python
## Coding Style
Set a coding style for your project:
https://google.github.io/styleguide/pyguide.html

## General best practices:
### Type hinting:
Typing
- https://docs.python.org/3/library/typing.html  
- https://peps.python.org/pep-0483/  

PEP conventions for designing classes, interfaces  
- https://peps.python.org/pep-0008/  
- https://peps.python.org/pep-0008/#naming-conventions  

### Python packaging:
Tool: https://github.com/audreyfeldroy/cookiecutter-pypackage  

Docstrings: https://peps.python.org/pep-0257/  

### Order of imports
- Python built-in first, then your pip ones, then your modules.  
- Avoid circular dependencies!  
- Rethink your structure if this ever happens.  
- All imports should be defined at the top of the file.  
- It should be avoided (this is also flake8 imposed).

### Writing classes
- Avoiding code duplication is nice BUT not at the expense of too many interface classes:
**Readability >>> Modularity**

- If things share similar “calls” then make a pure abstract class.  
- Inheritance more than two levels is typically bad for readability.  
- Don’t over-generalize until there are clear usecases in mind.  

### Handling configurations
- YAML vs JSON vs Python dataclasses
- This is a huge debate within the community as what is the best way to store configuration files
- Personal preference (Mayank): Python dataclasses
- Imposing a structure over configuration is nice because then you don’t define loose variables that are not used inside the code
- Gain a lot from IDE providing the config parameter in your class

- **YAML/JSON:**
    - Light-weight – use dicts for storage after parsed
    - Many tools already have ways to track experiments with these config files.

### Linting:
We use **flake8** for linting the python code:
```shell
# for checking lints
pip install flake8
flake8 .
```

### Formatting:

Use a code formatter!
We use **black** for formatting the python code: 
To run the formatter:

```shell
# for formatting
pip3 install black
black --line-length 120 .
```

### Virtual Environments

| **Tool**            | **Pros**                                                                             | **Cons**                                                                      |
| ------------------- | ------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------- |
| System Installation | ![#8fce00](https://via.placeholder.com/15/8fce00/000000?text=+) simple<br> ![#8fce00](https://via.placeholder.com/15/8fce00/000000?text=+) works with ROS                                                          | ![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+) cannot be shared<br> ![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+) dependecies problems when working on multiple projects |
| Conda               | ![#8fce00](https://via.placeholder.com/15/8fce00/000000?text=+) easy to setup and share<br> ![#8fce00](https://via.placeholder.com/15/8fce00/000000?text=+) wide adopted<br> ![#8fce00](https://via.placeholder.com/15/8fce00/000000?text=+) clear separation between projects | ![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+) works only with ROS with additional packages                                 |
| Virual Env          |                                                                                      |                                                                               |



## Usefulls Tools
### Logging 
For all ML-projects we highly recommend to use a logging framework.  
We suggest you to user either [NeptuneAI](https://neptune.ai/) or [Weights & Biases](https://wandb.ai/site).   
They are straight forward to integrate.  
On the cluster make sure to activate the proxy module.  

### Hyperparameter Optimization
We have good experience with using [Optuna](https://optuna.org/)



## Setting up a project
Installing your project as a package can provide quite a few benfits.   
This allows to easily avoid global pats and avoid import problems.
```yaml
project_name:
├──cfg:	
│    ├──env:
│    │   ├──my_machine.yml 
│    │   └──cluster.yml 
│    └──exp:
│        ├──exp_lr.yml 
│        └──exp_architecture.yml
│
├──project_name:
│    ├──network:
│    │   ├──network.py	
│    │   ├──__init__.py
│    ├──visualizer:
│    │   ├──visualizer.py
│    │   ├──__init__.py
│    └──utils:
│        └──__init__.py
│            
├──docs:
│    ├──overview.png
│    └──result.png
│        
├──scripts:
│    ├──train.py
│    ├──test.py
│    └──hyperparmeter.py 
│
├──setup.py
├──setup.cfg
├──.gitignore
├──README.md
```

```shell
pip3 install -e ./project_name
```





## IDE - VSCode Setup

### Debugging
Make sure to use all of the features or your IDE for debugging.
Read this [Tutorial](https://code.visualstudio.com/docs/editor/debugging) fully. This will save you a lot of time.
In vscode you can create a Debugging Configration as follows:
Open the `.vscode/launch.json`
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Debug Train Script TemplateProject",
            "type": "python",
            "request": "launch",
            "program": "/home/username/git/workflows/best-practices/python/template_project_name/scripts/train.py",
            "console": "integratedTerminal",
            "justMyCode": true,
            "pythonPath": "/home/username/miniconda3/envs/py38/bin/python3",
            "args": [
                "--exp=/path/to/something.yml",
                "--other=arg",
            ]
        },
    ]
}
```

Find the correct `pythonPath` by using the `which python3` command in your terminal.  
#### Checklist what you should be able to do:

- Creating Debugging Configurations
- Using Breakpoints
- Using the Debug Console
- Checking the Local Variable Scope
- Understanding the Call Stack



### Special Tricks

### Formatting

Get where black is installed:
```shell
python3 -c 'import black; from pathlib import Path; print(Path(black.__file__).parent)'
```

In VSCode `CTRL`+`Shift`+`P` edit your `settings.json`:
```json  
    "editor.formatOnSave": true,
    "python.formatting.blackPath": "~/.local/lib/python3.8/site-packages/black",
``` 

### Code Linting

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





