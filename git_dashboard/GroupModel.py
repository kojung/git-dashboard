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
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt

class GroupModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        """constructor"""
        super(GroupModel, self).__init__()
        self._data = data

    def data(self, index, role):
        """access model data"""
        if role == Qt.DisplayRole:
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        """number of rows"""
        return len(self._data)

    def columnCount(self, index):
        """number of columns"""
        return len(self._data[0])

    def headerData(self, col, orientation, role):
        """table header"""
        header = ["Name", "Status", "Path"]
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return header[col]
        return None

def test():
    """test function"""
    class MainWindow(QtWidgets.QMainWindow):
        def __init__(self, model):
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
    model.layoutAboutToBeChanged.emit()
    data.append(["baz", "up-to-date", "..."])  # show that data can change
    model.layoutChanged.emit()

    # main loop
    app.exec()

if __name__ == "__main__":
    test()
