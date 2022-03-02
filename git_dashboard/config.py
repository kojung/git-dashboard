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
from git import Repo, InvalidGitRepositoryError, NoSuchPathError

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

def short_sha(sha):
    """return a shorter sha signature"""
    return str(sha)[0:8]

def analyze(path):
    """
    given a path to a git repository, return:
    [name, branch, status]
    """
    name = os.path.basename(path)
    try:
        repo = Repo(path)
        head = repo.head
        if head.is_detached:
            branch = f"detached:{short_sha(head.commit)}"
        else:
            branch = head.reference.name
        return [name, branch, "status", path]  # WIP
    except (InvalidGitRepositoryError, NoSuchPathError):
        return [name, "n/a", "not a git repo", path]

def load_configuration():
    """load configuration"""
    with open(CONFIG, "r", encoding="utf-8") as cfg:
        groups = yaml.safe_load(cfg)

    # iterate through each group and do:
    # 1. expand paths that contain other git repos
    # 2. analyze git repos
    results = {}
    for name, group in groups.items():
        # expand directories that contain other git repos
        results[name] = []
        for dirname in group:
            _, dirnames, _ = next(os.walk(dirname))
            if ".git" not in dirnames:
                for sub_repo in find_git_repos_from_path(dirname, 0, 1):
                    results[name].append(analyze(sub_repo))
            else:
                results[name].append(analyze(dirname))
    return results
