# Formatting 
Auto formatting reduces the burden to clean up code and increases readability.
We recommend here formatters available for development with VSCode.


## Python - Black
We use black formatter for formatting the python code. 
To run the formatter:

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

## CPP - Clang-Format
Install the `Clang-Format` Extension in VSCode.
Use the Google Formatting option.
Example `.clang-format` file is provided at `best-practices/formatting/.clang-format`.
Set as default in `settings.json`:
```json
    "[cpp]": {
        "editor.defaultFormatter": "xaver.clang-format"
    },
```

## XML
Standard XML Language Support by Red Hat Extension in VSCode.  
Set as default in `settings.json`:
```json
    "[xml]": {
        "editor.defaultFormatter": "redhat.vscode-xml"
    },
    "xml.format.emptyElements": "collapse",
    "xml.format.joinCDATALines": true,

```

## YAML 
Standard YAML Language Support by Red Hat Extension in VSCode.
Set as default in `settings.json`:  
```json
    "[yaml]": {
        "editor.defaultFormatter": "redhat.vscode-yaml"
    }
```