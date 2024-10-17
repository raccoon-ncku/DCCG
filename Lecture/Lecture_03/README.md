# Lecture 03: COMPAS Core
## Slides
👉[Slides](https://app.rccn.dev/slidev/DCCG-03)

## Installing COMPAS

> [!IMPORTANT]
> Please follow the written instructions carefully. Type or copy and paste the commands provided, rather than relying solely on the images. While the images are helpful, they may not be updated as frequently as the text. 

Open `Anaconda Powershell Prompt (miniconda3)` (Windows), or `Powershell` (Windows),  or `Terminal` (macOS).

First, we have to add `conda-forge` as a channel for `conda` to fetch packages. This only needs to be done once on every computer.
```
conda config --add channels conda-forge
```
If the command return nothing, it means the channel has been added successfully.

Next, create a new environment for this course:
```
conda create -n DCCG compas
```
![conda_create_env](/Assets/imgs/conda_create.png)

When prompted, type `y` to proceed.
![conda_create_env](/Assets/imgs/conda_create_prompt.png)

When finished, activate the environment, so that we could install packages into it.
```
conda activate DCCG
```
![conda_activate_env](/Assets/imgs/conda_activate.png)

When an environment is activated, the name of the environment will be shown in front of the command prompt. In this case, it is `(DCCG)`. Continue to install COMPAS_viewer:
```
pip install compas_viewer
```
![conda_install_compas](/Assets/imgs/conda_install_warning.png)

These step might take a while. You might experience a warning like this. It is because the some module we use is not yet a stable version. When prompted, type `y` to proceed.
![conda_install_compas](/Assets/imgs/conda_install_prompt.png)

## Verify COMPAS installation
When finished, test if the installation is successful. Go back to vscode and open the example `Lecture/Lecture_03/compas_core_examples_I/1.4.2_visualization_II.py`. Check the bottom right corner of the window. If it shows `Python 3.12.7 64-bit ('DCCG': conda)`, it means the script will be executed in the correct environment. If not, click the Python version and select `DCCG: conda`.

![vscode_select_env](/Assets/imgs/vscode_python_interpreter.png)

Once the correct environment is selected, click the `Run` button on the top right corner of the window. If the installation is successful, you should see a window like this:

![vscode_run](/Assets/imgs/compas_viewer.png)


## Installing COMPAS for Rhino

> [!IMPORTANT]
> The section on integrating Rhino with COMPAS has been temporarily removed for the Class of 2024. At the time of writing, there are ongoing transitions, such as from Rhino 7 to 8 and from IronPython to CPython. Additionally, Rhino integration is not heavily utilized in this course.

## Conda init issue

Windows:
Open Powershell and type `$PROFILE`, manually edit the `.ps1` file with the following code.

```

#region conda initialize
# !! Contents within this block are managed by 'conda init' !!
(& "%UserProfile%\miniconda3\Scripts\conda.exe" "shell.powershell" "hook") | Out-String | Invoke-Expression
#endregion


```