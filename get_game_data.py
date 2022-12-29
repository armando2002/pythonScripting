# handle OS functions
import os
# handle json
import json
# allow copy and overwrite ops
import shutil
# run any terminal commands
from subprocess import PIPE, run
# get access to command line arguments
import sys

# look for string 'game' in directories
GAME_DIR_PATTERN = "game"


def find_all_game_dirs(source):
    game_paths = []
    # walk the source path
    for root, dirs, files in os.walk(source):
        for directory in dirs:
            if GAME_DIR_PATTERN in directory.lower():
                path = os.path.join(source, directory)
                game_paths.append(path)
        break

    return game_paths


def get_name_from_paths(paths, to_strip):
    new_names = []
    for path in paths:
        _, dir_name = os.path.split(path)
        new_dir_name = dir_name.replace(to_strip, "")
        new_names.append(new_dir_name)

    return new_names


def create_dir(path):
    # if directory doesn't exist, create it
    if not os.path.exists(path):
        os.mkdir(path)


def copy_and_overwrite(source, dest):
    if os.path.exists(dest):
        # remove destination folder using remove tree
        shutil.rmtree(dest)
    # copy the tree
    shutil.copytree(source, dest)


def make_json_metadata_file(path, game_dirs):
    data = {
        "gameNames": game_dirs,
        "numberOfGames": len(game_dirs)
    }
    # write into a json file
    with open(path, "w") as f:
        json.dump(data, f)


def main(source, target):
    # get current working directory (where the python file was run from)
    cwd = os.getcwd()
    # set source and target paths
    source_path = os.path.join(cwd, source)
    target_path = os.path.join(cwd, target)

    game_paths = find_all_game_dirs(source_path)
    new_game_dirs = get_name_from_paths(game_paths, "_game")
    # create directory
    create_dir(target_path)

    # loop through the source and destination paths
    # zip takes matching elements from 2 arrays and puts them together in a tuple
    for src, dest in zip(game_paths, new_game_dirs):
        dest_path = os.path.join(target_path, dest)
        copy_and_overwrite(src, dest_path)
    # set the path for the JSON to be with in the target directory
    json_path = os.path.join(target_path, "metadata.json")
    # make the JSON file
    make_json_metadata_file(json_path, new_game_dirs)


# grab the command line arguments only if this program is being run directly, not imported
if __name__ == "__main__":
    # check the # of arguments sent
    args = sys.argv
    if len(args) != 3:
        raise Exception("You must pass a source and target directory.")
    # get the 2 arguments after *.py
    source, target = args[1:]
    main(source, target)


