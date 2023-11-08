import os

# Current working directory where the Python interpreter is started
CWD = os.getcwd()
# The path of the current file
FILE = __file__
# The directory of the current file
FILE_DIR = os.path.dirname(__file__)

with open('result.md', 'w') as fp:
    fp.write(
        "The current working directory(`os.getcwd()`) is:\n{}\n\n".format(
            CWD, FILE_DIR
        )
    )
    fp.write(
        "The file path (`__file__`) is:\n{}\n\n".format(FILE)
    )
    fp.write(
        "The file directory (`os.path.dirname(__file__)`) is:\n{}".format(FILE_DIR)
    )
