# Class 
## Slides
👉[Slides](https://docs.google.com/presentation/d/1gCXsjg1PCO-fWoE2ojZQB80b2N2oioUNpyTs6SwSko8/edit?usp=sharing)

## Installing COMPAS
Open `Anaconda Powershell Prompt (miniconda3)` (Windows), or `Powershell` (Windows),  or `Terminal` (macOS).

First, we have to add `conda-forge` as a channel for `conda` to fetch packages. This only needs to be done once on every computer.
```
conda config --add channels conda-forge
```

Next, activate the environment and install the packages:
```
conda activate DCCG
conda install compas compas_view2
```
Before the last step, make sure the scripting interface of Rhino has been initialized at least once. This only needs to be done once on every computer. To do that, open Rhino and navigate to `Tools > PythonScript > Edit...`. Once the script editor shows up, the interface is successfully initialized, and Rhino could be closed.

Finally, depending on your installed Rhino version, execute one of the flollowing:

#### Rhino 6
```
python -m compas_rhino.install -v 6.0
```

#### Rhino 7
```
python -m compas_rhino.install -v 7.0
```


## Verify Installation


### Python and Rhino
Check if the tab COMPAS exists in Grasshopper. Place the `info` component on the canvas to get more information.
![compas_installed_in_rhino](Assets/img/compas_installed_in_rhino.png)
    
## Using COMPAS and VScode along with Rhino/GH
Open and __save__ Grasshopper file. 
Copy the following codes into a Grasshopper Python Component.
Adjust the component setting as instructed.

```Python
"""
Get the path of files in the same folder with this GH file.
If filename is omitted, this will return the path of this GH file.

Please configure the Grasshopper component's parameters as the following:
Input:
    - filename: list_access, type_hint: str
Output:
    - path
    - file
"""

import Grasshopper
import os

filepath = ghenv.Component.OnPingDocument().FilePath
path = os.path.dirname(filepath)
if filename:
    path = os.path.join(path, *filename)


file = None
if os.path.isfile(path):
    with open(path) as f:
        file = f.read()
```

## Conda init issue

Windows:
Open Powershell and type `$PROFILE`, manually edit the `.ps1` file with the following code.

```

#region conda initialize
# !! Contents within this block are managed by 'conda init' !!
(& "%UserProfile%\miniconda3\Scripts\conda.exe" "shell.powershell" "hook") | Out-String | Invoke-Expression
#endregion


```