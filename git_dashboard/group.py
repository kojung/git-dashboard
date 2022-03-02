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
Group Model and View classes

A group is a collection of related repos. Underlying model is just a list of
repo paths:

group = [
    ["path1"],
    ["path2"],
    ...
]

The group model is in charge of expanding the path into name, branch, status, and
other useful information to the view component.
"""

import sys
import os

from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt
from git import Repo, InvalidGitRepositoryError, NoSuchPathError

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

class GroupModel(QtCore.QAbstractTableModel):
    """Model Group"""
    def __init__(self, group):
        """Constructor"""
        super().__init__()
        self.header = ["name", "branch", "status", "path"]
        self.group = group

    def data(self, index, role):
        """access model data"""
        if role == Qt.DisplayRole:
            columns = analyze(self.group[index.row()])
            return columns[index.column()]
        return None

    def rowCount(self, _):
        """number of rows"""
        return len(self.group)

    def columnCount(self, _):
        """number of columns"""
        return len(self.header)

    def headerData(self, col, orientation, role):
        """table header"""
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None

class GroupView(QtWidgets.QTableView):
    """View for group"""
    def __init__(self, model):
        """constructor"""
        super().__init__()
        self.setModel(model)

        # make columns resizable
        header = self.horizontalHeader()
        modes = [
            QtWidgets.QHeaderView.ResizeToContents,  # name
            QtWidgets.QHeaderView.ResizeToContents,  # branch
            QtWidgets.QHeaderView.ResizeToContents,  # status
            QtWidgets.QHeaderView.Stretch,           # path
        ]
        for idx, mode in enumerate(modes):
            header.setSectionResizeMode(idx, mode)

def main():
    """test function"""
    class MainWindow(QtWidgets.QMainWindow):
        """main window"""
        def __init__(self, view):
            """constructor"""
            super().__init__()
            self.setCentralWidget(view)

    # data for group
    script_dir = os.path.dirname(__file__)
    parent_dir = os.path.realpath(os.path.join(script_dir, ".."))
    group = [parent_dir, parent_dir, parent_dir]

    # table model
    app    = QtWidgets.QApplication(sys.argv)
    model  = GroupModel(group)
    view   = GroupView(model)
    window = MainWindow(view)
    window.show()

    # show that model can change after show()
    model.layoutAboutToBeChanged.emit() # pylint: disable=no-member
    group.append(repo_path)             # show that data can change
    model.layoutChanged.emit()          # pylint: disable=no-member

    # main loop
    app.exec()

if __name__ == "__main__":
    main()
