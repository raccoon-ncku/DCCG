# Optimization with OR-Tools
There are plenty of modules for optimization in Python. One of the most popular is [OR-Tools](https://developers.google.com/optimization). It is a Google product and is open source. It is also available in many other programming languages.

Although we could install OR-Tools in our DCCG environment, we will create a new environment for OR-Tools to simplify the installation time. 

```bash
conda create -n ortools python=3.9
conda activate ortools
python -m pip install --upgrade --user ortools
```