# Class Materials


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
    
