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
Tab view
"""

import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTabWidget,
)

from git_dashboard.group_model import GroupModel

class GroupsView(QTabWidget):
    """
    Groups view
    data consists of a dictionary of group name and group data. E.g.:
    {
        "group1": [["repo1", "status1", "path1"]],
        "group2": [["repo2", "status2", "path2"],
                   ["repo2", "status2", "path2"]]
    }
    """
    def __init__(self, groups):
        """constructor"""
        super().__init__(self, groups)
        self.groups = groups

def main():
    """main routine for test purposes"""
    class MainWindow(QMainWindow):
        """main window"""
        def __init__(self, model):
            """constructor"""
            super().__init__()

            tabs = QTabWidget()
            tabs.setTabPosition(QTabWidget.West)
            tabs.setMovable(True)

            for name, group in model.items():
                tabs.addTab(GroupModel(group), name)

            self.setCentralWidget(tabs)

    app = QApplication(sys.argv)

    model = {
        "project1": [
            ["foo", "up-to-date", "..."],
            ["bar", "-1, +100", "..."],
        ],
        "project2": [
            ["baz", "up-to-date", "..."],
        ],
    }
    window = MainWindow(model)
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
