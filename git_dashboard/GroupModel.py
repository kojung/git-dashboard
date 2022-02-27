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
        super(GroupModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])


def test(data):
    """test function"""
    class MainWindow(QtWidgets.QMainWindow):
        def __init__(self, data):
            super().__init__()
            self.table = QtWidgets.QTableView()
            self.model = GroupModel(data)
            self.table.setModel(self.model)
            self.setCentralWidget(self.table)

    app=QtWidgets.QApplication(sys.argv)
    window=MainWindow(data)
    window.show()
    app.exec()

if __name__ == "__main__":
    data = [
      [4, 9, 2],
      [1, 0, 0],
      [3, 5, 0],
      [3, 3, 2],
      [7, 8, 9],
    ]

    test(data)
