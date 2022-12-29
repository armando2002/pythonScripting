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


def main(source, target):
    # get current working directory (where the python file was run from)
    cwd = os.getcwd()
    # set source and target paths
    source_path = os.path.join(cwd, source)
    target_path = os.path.join(cwd, target)

    game_paths = find_all_game_dirs(source_path)
    print(game_paths)


# grab the command line arguments only if this program is being run directly, not imported
if __name__ == "__main__":
    # check the # of arguments sent
    args = sys.argv
    if len(args) != 3:
        raise Exception("You must pass a source and target directory.")
    # get the 2 arguments after *.py
    source, target = args[1:]
    main(source, target)


