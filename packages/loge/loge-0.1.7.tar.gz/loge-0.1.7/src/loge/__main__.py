# -*- coding: utf-8 -*-
#-----------------------------------------------------------------
# Copyright (C) 2017, the Loge development team
#
# This file is part of Loge
# Loge is distributed under the terms of GNU General Public License
# The full license can be found in 'license.txt'
# Loge development team can be found in 'development.txt'
#-----------------------------------------------------------------

"""
This module takes enables starting Loge via either "python -m loge" or "python path/to/loge"
"""

import sys
import os

from PyQt5.QtWidgets import QApplication

"""
If loge package not instaled we need to add parent directory to sys.path
"""
try:
    import loge
except ImportError:
    _this_dir = os.path.abspath(os.path.dirname(__file__))
    sys.path.insert(0, os.path.split(_this_dir)[0])

from loge.gui.Gui import Gui
from loge.core.Core import Core
from loge.memos import appinfo

def main():
    app = QApplication(sys.argv)
    CORE = Core()
    WINDOW = Gui(appinfo.name, appinfo.version)
    #---
    WINDOW.connect_to_core(CORE)
    #---
    WINDOW.main_window.closeEvent = WINDOW.closeEvent
    WINDOW.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()