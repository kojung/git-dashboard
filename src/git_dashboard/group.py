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
repo attributes:

group = [
    ["name1", "branch1", "status1", "path1"],
    ["name2", "branch2", "status2", "path2"],
    ...
]

The group model is in charge of expanding the path into name, branch, status, and
other useful information to the view component.
"""

import re

from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt, QSortFilterProxyModel
from PySide6.QtGui import QFont

class GroupModel(QtCore.QAbstractTableModel):
    """Model Group"""
    def __init__(self, group):
        """Constructor"""
        super().__init__()
        self.header = ["name", "branch", "status", "path"]
        self.group = group

    def data(self, index, role): # pylint: disable=too-many-return-statements
        """access model data"""
        # DisplayRole
        if role == Qt.DisplayRole:
            return self.group[index.row()][index.column()]

        # Color
        if index.isValid() and role == Qt.ForegroundRole:
            # branch color
            if index.column() == 1:
                if re.search(r'master|develop', index.data()):
                    return QtGui.QBrush(QtCore.Qt.darkGreen)
                return QtGui.QBrush(QtCore.Qt.black)

            # status color
            if index.column() == 2:
                if index.data() == "clean":
                    return QtGui.QBrush(QtCore.Qt.darkGreen)
                if index.data() == "dirty":
                    return QtGui.QBrush(QtCore.Qt.darkRed)
                if index.data() == "untracked":
                    return QtGui.QBrush(QtCore.Qt.blue)
                return QtGui.QBrush(QtCore.Qt.black)

        # Color for branches
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

        # enable sorting through a proxy model
        self.setSortingEnabled(True)
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(model)
        self.setModel(self.proxy_model)

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

        # set font size
        self.setFont(QFont("Arial", 8))
