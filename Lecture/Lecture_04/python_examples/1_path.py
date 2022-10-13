import os

# Current working directory
CWD = os.getcwd()
print("Current working directory is:\n{}\n".format(CWD))
# The directory the Python file is contained in
F = os.path.dirname(__file__)
print("The directory the Python file is contained in is:\n{}".format(F))
