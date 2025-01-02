## Basic Machine Learning and Optimization

### Basic Machine Learning
👉[Slides](https://app.rccn.dev/slidev/DCCG-09)

### Basic Optimization
👉[Slides](https://app.rccn.dev/slidev/DCCG-09)

## Optimization with OR-Tools
There are plenty of modules for optimization in Python. One of the most popular is [OR-Tools](https://developers.google.com/optimization). It is a Google product and is open source. It is also available in many other programming languages.

Although we could install OR-Tools in our DCCG environment, we will create a new environment for OR-Tools to simplify the installation time. 

```bash
conda create -n DCCG-optim python=3.9 deap pymoo scikit-learn
conda activate DCCG-optim
python -m pip install ortools
```