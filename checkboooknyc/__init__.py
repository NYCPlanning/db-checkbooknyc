import os

from dotenv import load_dotenv

# Load environmental variables
load_dotenv()


BUILD_ENGINE = os.environ["BUILD_ENGINE"]

base_path = ".output"
if not os.path.isdir(base_path):
    os.makedirs(base_path, exist_ok=True)
    # create .gitignore so that files in this directory aren't tracked
    with open(f"{base_path}/.gitignore", "w") as f:
        f.write("*")
