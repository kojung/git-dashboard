# Git Dashboard
# Copyright (C) 2022 Jung Ko <kojung@gmail.com>
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of  MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Configuration functionality

Configuration is stored as a YAML file with the following format:

"""

import os
from pathlib import Path
import copy

from appdirs import user_config_dir
import yaml

import git_dashboard

CONFIG_DIR = user_config_dir(git_dashboard.__name__, git_dashboard.__author__)
CONFIG = os.path.join(CONFIG_DIR, "config.yaml")

def find_git_repos_from_path(dirname, depth=0, maxdepth=-1):
    """
    recursively find all git repos given the path. stop recusion when `depth == maxdepth`
    """
    results = []
    dirpath, dirnames, _ = next(os.walk(dirname))
    if ".git" in dirnames:
        return [dirpath]
    if depth != maxdepth:
        for name in dirnames:
            absname = os.path.join(dirname, name)
            results += find_git_repos_from_path(absname, depth+1, maxdepth)
    return results

def create_default_configuration(root):
    """scan for git repos starting from root"""
    print(f"Scanning git repos from '{root}': ", end='')
    repos = {'home': find_git_repos_from_path(root)}
    print(f"found {len(repos['home'])} git repos")
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG, "w", encoding="utf-8") as cfg:
        yaml.dump(repos, cfg)

def load_configuration():
    """load configuration"""
    with open(CONFIG, "r", encoding="utf-8") as cfg:
        groups = yaml.safe_load(cfg)
    for group in groups.values():
        expanded_dirs = []
        group_copy    = copy.copy(group)
        # loop through each group and expand directories if needed
        # use a copy of the group because we are modifing the list as we iterate through the list
        for dirname in group_copy:
            _, dirnames, _ = next(os.walk(dirname))
            if ".git" not in dirnames:
                expanded_dirs += find_git_repos_from_path(dirname, 0, 1) 
                group.remove(dirname)
        group += expanded_dirs

    return groups

def main():
    """for test purposes"""
    home = Path.home()
    create_default_configuration(home)
    print(f"Created default configuration at '{CONFIG}'")

if __name__ == "__main__":
    main()
