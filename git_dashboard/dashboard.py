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
Git Dashboard
"""

import os
import sys
import signal
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)

from git_dashboard.groups import GroupsView
from git_dashboard.config import (
    CONFIG,
    create_default_configuration,
    load_configuration,
)

class MainWindow(QMainWindow):
    """main window"""
    def __init__(self, view):
        """constructor"""
        super().__init__()
        self.setCentralWidget(view)

def sigint_handler(*args): # pylint: disable=unused-argument
    """Handler for the SIGINT signal."""
    QApplication.quit()

def main():
    """main routine for test purposes"""
    # create default configuration if needed
    if not os.path.exists(CONFIG):
        home = Path.home()
        create_default_configuration(home)

    # capture ctrl-c signal so we can exit gracefully
    signal.signal(signal.SIGINT, sigint_handler)

    # start the app
    app    = QApplication(sys.argv)

    # model and views
    groups = load_configuration()
    view   = GroupsView(groups)
    window = MainWindow(view)

    # resize primary window to 1/3 width + 1/2 height
    screen = app.primaryScreen()
    size   = screen.size()
    window.resize(size.width()//3, size.height()//2)

    window.show()
    app.exec()

if __name__ == "__main__":
    main()
