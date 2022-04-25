"""Generate a YAML file with default messages and specific paths."""
from importlib.resources import path
import os
# Import the necessary libraries


# First, iterate the paths
# Only target the paths where the key word shows up in the first or second level
# Combine paths with files to create the complete paths
# Put paths into a list

def create_targeted_paths_list():
    """Generate a list of targeted paths by walking the paths."""
    targeted_paths = []
    key_word_list = ["writing", "src", "test"]
    # Go through the root repo, the sub dictionaries and files.
    # The os.walk will only scan the paths. So the empty folders containing nothing won't be gone through.
    for dirpath, _, filenames in os.walk("."):
        for filename in filenames:
            # Split path string to split it into multiple directories.
            path_dir_list = dirpath.split("/")
            # The first directory is always dot, so skip it.
            if len(path_dir_list) == 1:
                continue
            # Ignore hidden folders.
            if path_dir_list[1].startswith("."):
                continue

            # Add paths only when they have the key words in the second and the third directories.
            elif len(path_dir_list) == 2:
                for key in key_word_list:
                    # For the path with only two directories, check key words in the second directory folder name.
                    if key in path_dir_list[1]:
                        targeted_paths.append(os.path.join(dirpath, filename))

            # For the other paths with more than 2 directories, check key words in the second and third directories.
            else:
                for key in key_word_list:
                    if key in path_dir_list[1] or key in path_dir_list[2]:
                        targeted_paths.append(os.path.join(dirpath, filename))
    return targeted_paths

def write_yaml_of_paths_list(path_names):
    """Write YAML file to create gatorgrade file and set default messages."""
    # Create a new YAML file with PyYaml in the specific path.
    # write the default set up messages in YAML file.
    # List the file paths in specific format.
    pass

print(create_targeted_paths_list())