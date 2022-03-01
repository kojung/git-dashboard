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
Groups is a collection of Group (see group.py). Underlying model is a dictionary
of groups. E.g.
    groups = {
        "group1": [["path1"]],
        "group2": [["path2"],
                   ["path3"]]
    }
"""

import sys
import os

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTabWidget,
)

from git_dashboard.group import (
    GroupView,
    GroupModel
)

class GroupsView(QTabWidget):
    """View class for groups"""
    def __init__(self, groups):
        """constructor"""
        super().__init__()
        self.groups = groups

        self.setTabPosition(QTabWidget.West)
        self.setMovable(True)

        for name, group in groups.items():
            model = GroupModel(group)
            view  = GroupView(model)
            self.addTab(view, name)

def main():
    """main routine for test purposes"""
    class MainWindow(QMainWindow):
        """main window"""
        def __init__(self, view):
            """constructor"""
            super().__init__()
            self.setCentralWidget(view)

    app = QApplication(sys.argv)

    this_script = os.path.realpath(__file__)
    repo_path   = os.path.join(this_script, "..")

    model = {
        "project1": [repo_path, repo_path, repo_path],
        "project2": [repo_path],
    }
    view   = GroupsView(model)
    window = MainWindow(view)
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
