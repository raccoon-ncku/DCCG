"""
Paths — the essentials, using pathlib.

The old way was `os.path.join`, `os.getcwd`, `os.path.dirname(__file__)`.
It works, but you glue strings together and every OS quirk becomes yours.
The README says "use pathlib, always" — this file shows why.
"""

from pathlib import Path

# --- where am I? ----------------------------------------------------------

# The folder your terminal is in when you launched the script.
CWD = Path.cwd()
print(f"cwd:        {CWD}")

# The script file itself. `__file__` is a string; wrap it in Path().
THIS_FILE = Path(__file__)
print(f"this file:  {THIS_FILE}")
print(f"this dir:   {THIS_FILE.parent}")


# --- joining paths — the / operator ---------------------------------------

# Never build paths by gluing strings with "/" or "\\" — that breaks
# between Windows and macOS, and it is the reason half of all "works on
# my machine" problems exist.
folder = Path("data")
file   = folder / "result.json"      # data/result.json on any OS
print(f"joined:     {file}")


# --- inspecting a path ----------------------------------------------------

print(f"name:       {file.name}")     # 'result.json'
print(f"stem:       {file.stem}")     # 'result'
print(f"suffix:     {file.suffix}")   # '.json'
print(f"parent:     {file.parent}")   # 'data'


# --- existence and creation -----------------------------------------------

# folder.exists()      — bool
# folder.is_dir()      — is it a directory
# folder.is_file()     — is it a regular file
# folder.mkdir(parents=True, exist_ok=True) — create it, no error if present

output = THIS_FILE.parent / "data" / "output"
output.mkdir(parents=True, exist_ok=True)
print(f"created:    {output}")
