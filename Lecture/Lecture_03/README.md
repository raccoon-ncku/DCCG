# Lecture 03: COMPAS Core
## Slides
👉[Slides: Compas Core](https://app.rccn.dev/slidev/DCCG-03)

👉[Slides: Transformation](https://app.rccn.dev/slidev/DCCG-03-1)

## Installing COMPAS

> [!IMPORTANT]
> Please follow the written instructions carefully. Type or copy and paste the commands provided, rather than relying solely on the images. While the images are helpful, they may not be updated as frequently as the text. 

Open `Anaconda Powershell Prompt (miniconda3)` (Windows), or `Powershell` (Windows),  or `Terminal` (macOS).

First, we have to add `conda-forge` as a channel for `conda` to fetch packages. This only needs to be done once on every computer.
```
conda config --add channels conda-forge
```
If the command return nothing, it means the channel has been added successfully.

Next, create a new environment for this course, and here we explicitly specify the Python version to be `3.9.10`, which is the version shipped with Rhino 8.
```
conda create -n DCCG python=3.9.10 compas pyside6
```
![conda_create_env](/Assets/imgs/conda_create.png)

> note: As of Oct 2025, `pyside6` need to be explicitly installed for `compas_viewer` to be `pip` installed correctly.

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
When finished, test if the installation is successful. Go back to vscode and open the example `Lecture/Lecture_03/compas_core_examples_I/1.4.2_visualization_II.py`. Check the bottom right corner of the window. If it shows `Python 3.9.10 64-bit ('DCCG': conda)` or similar, it means the script will be executed in the correct environment. If not, click the Python version and select `DCCG: conda`.

![vscode_select_env](/Assets/imgs/vscode_python_interpreter.png)

Once the correct environment is selected, click the `Run` button on the top right corner of the window. If the installation is successful, you should see a window like this:

![vscode_run](/Assets/imgs/compas_viewer.png)


## Installing COMPAS for Rhino

> [!IMPORTANT]
> This section is still under investigation, will be updated soon.

## Troubleshooting

If you already have conda isntalled a while ago, you might encounter some issues installing packages.
In this case, try to reset the conda-forge channel by running the following commands:

```bash
conda config --remove channels conda-forge
conda config --add channels conda-forge
conda clean --all
conda update -n base conda
```

Then try to create the environment again.

```bash
conda create -n DCCG python=3.9.10 compas pyside6
conda activate DCCG
pip install compas_viewer
```