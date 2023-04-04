#Just correctly runnig the main.py file
import os

# Get the absolute path to the directory containing this script
script_dir = os.path.normcase(os.path.abspath(os.path.dirname(__file__)))

# Get the current working directory
current_dir = os.path.normcase(os.getcwd())

# Check if the script is being run from the root directory
if script_dir != current_dir:
    print("Please run PLAY.py from the repository's root directory.")
else:
    # Launch the main.py file
    os.system("python3 ./src/main.py")
