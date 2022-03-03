#!/usr/bin/env python3

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
import functools
import argparse

from PySide6.QtCore import QTimer
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

def refresh(view, config):
    """refresh repo status"""
    groups = load_configuration(config)
    for name, model in view.models.items():
        model.layoutAboutToBeChanged.emit()        # pylint: disable=no-member
        model.group = groups[name]
        model.layoutChanged.emit()                 # pylint: disable=no-member

def parser():
    """argument parser"""
    par = argparse.ArgumentParser(description="Git dashboard")
    par.add_argument("-r", "--refresh",  type=int, default=10, help="Refresh interval in seconds. Default=10")
    par.add_argument("-c", "--config",  default=CONFIG, help=f"Configuration file. Default={CONFIG}")
    return par

def main():
    """main routine for test purposes"""
    args = parser().parse_args()

    # create default configuration if needed
    if not os.path.exists(args.config):
        home = Path.home()
        create_default_configuration(home, 'home', args.config)

    # capture ctrl-c signal so we can exit gracefully
    signal.signal(signal.SIGINT, sigint_handler)

    # start the app
    app    = QApplication(sys.argv)

    # model and views
    groups = load_configuration(args.config)
    view   = GroupsView(groups)
    window = MainWindow(view)

    # status refresh rate
    refresh_callback = functools.partial(refresh, view=view, config=args.config)

    timer = QTimer()
    timer.start(args.refresh * 1000)  # in milliseconds
    timer.timeout.connect(refresh_callback)  # pylint: disable=no-member

    # resize primary window to 1/3 width + 1/2 height
    screen = app.primaryScreen()
    size   = screen.size()
    window.resize(size.width()//3, size.height()//2)

    window.show()
    app.exec()

if __name__ == "__main__":
    main()
