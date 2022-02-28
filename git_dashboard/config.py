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
from appdirs import user_config_dir
import yaml

import git_dashboard

CONFIG_DIR = user_config_dir(git_dashboard.__name__, git_dashboard.__author__)
CONFIG = os.path.join(CONFIG_DIR, "config.yaml")

def create_default_configuration(root):
    """scan for git repos starting from root"""
    repos = []
    for dirpath, dirnames, filenames in os.walk(root):
        if ".git" in dirnames:
            repos.append(dirpath)
    with open(CONFIG, "w", encoding="utf-8") as cfg:
        yaml.dump(repos, cfg)

def main():
    """for test purposes"""
    create_default_configuration(os.environ.get("HOME"))

if __name__ == "__main__":
    main()
