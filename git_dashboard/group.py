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

A group is a collection of related repos. Underlying model is a 2D array:

group = [
    ["name1", "status1", "path1"],
    ["name2", "status2", "path2"],
    ...
]
"""

import sys
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt

class GroupModel(QtCore.QAbstractTableModel):
    """Model Group"""
    def __init__(self, group):
        """Constructor"""
        super().__init__()
        self.header = ["Name", "Status", "Path"]
        self.group = group

    def data(self, index, role):
        """access model data"""
        if role == Qt.DisplayRole:
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self.group[index.row()][index.column()]
        return None

    def rowCount(self, _):
        """number of rows"""
        return len(self.group)

    def columnCount(self, _):
        """number of columns"""
        return len(self.group[0])

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

def main():
    """test function"""
    class MainWindow(QtWidgets.QMainWindow):
        """main window"""
        def __init__(self, view):
            """constructor"""
            super().__init__()
            self.setCentralWidget(view)

    # data for group
    group = [
      ["foo", "up-to-date", "..."],
      ["bar", "-1, +100", "..."],
    ]

    # table model
    app    = QtWidgets.QApplication(sys.argv)
    model  = GroupModel(group)
    view   = GroupView(model)
    window = MainWindow(view)
    window.show()

    # notify model that data is about to change
    model.layoutAboutToBeChanged.emit()        # pylint: disable=no-member
    group.append(["baz", "up-to-date", "..."]) # show that data can change
    model.layoutChanged.emit()                 # pylint: disable=no-member

    # main loop
    app.exec()

if __name__ == "__main__":
    main()
