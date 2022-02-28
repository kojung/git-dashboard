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
Group View
"""

import sys
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt

class GroupModel(QtCore.QAbstractTableModel):
    """
    Model representing a group of repositories using a 2D list:
    [["name1", "status1", "path1"],
     ["name2", "status2", "path2"],
     ...
    ]
    """
    def __init__(self, data):
        """constructor"""
        super().__init__()
        self.header = ["Name", "Status", "Path"]
        self._data = data

    def data(self, index, role):
        """access model data"""
        if role == Qt.DisplayRole:
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]
        return None

    def rowCount(self, _):
        """number of rows"""
        return len(self._data)

    def columnCount(self, _):
        """number of columns"""
        return len(self._data[0])

    def headerData(self, col, orientation, role):
        """table header"""
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None

def main():
    """test function"""
    class MainWindow(QtWidgets.QMainWindow):
        """main window"""
        def __init__(self, model):
            """constructor"""
            super().__init__()
            table = QtWidgets.QTableView()
            table.setModel(model)
            self.setCentralWidget(table)

    # data underneath the model
    data = [
      ["foo", "up-to-date", "..."],
      ["bar", "-1, +100", "..."],
    ]

    # table model
    model  = GroupModel(data)
    app    = QtWidgets.QApplication(sys.argv)
    window = MainWindow(model)
    window.show()

    # notify model that data is about to change
    model.layoutAboutToBeChanged.emit()        # pylint: disable=no-member
    data.append(["baz", "up-to-date", "..."])  # show that data can change
    model.layoutChanged.emit()                 # pylint: disable=no-member

    # main loop
    app.exec()

if __name__ == "__main__":
    main()
