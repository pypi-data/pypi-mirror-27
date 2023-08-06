# -*- coding: utf-8 -*-
#--------------------------------------------------------------------
# Copyright (C) 2017, the Loge development team
#
# This file is part of Loge
# Loge is distributed under the terms of GNU General Public License
# The full license can be found in 'license.txt'
# Loge development team can be found in 'development.txt'
#--------------------------------------------------------------------

"""
---------------------------------------------------------------------
A module containing utilities.
---------------------------------------------------------------------
"""

from pkg_resources import resource_string

from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QCoreApplication

TR_GUI_CONTEXT = 'Gui'

def translate(context,msg):
    return QCoreApplication.translate(context,msg)

def get_icon(icon_name):
    """
    Creates an icon from file.
    
    Args:
        icon_name (str): the name of an icon file

    Retruns:
        QIcon: An icon object
    """
    pixmap = QPixmap()
    pixmap.loadFromData(resource_string(__name__, '/icons/{}'.format(icon_name)))
    icon = QIcon(pixmap)
    return icon

def create_action(icon_name,act_name,shortcut,tip,parent):
    """
    Creates an action object.
    
    Args:
        icon_name (str):    a name of an icon file
        act_name (str):     an action name
        shortcut (str):     a shortcut string or QKeySequence standart shortcut
        tip (str):          a tip text
        parent (obj):       a parent object instance

    Retruns:
        QAction: An icon object
    """
    action = QAction(act_name,parent)
    if icon_name is not None:
        action.setIcon(get_icon(icon_name))
    if shortcut is not None:
        action.setShortcut(shortcut)
    if tip is not None:
        action.setToolTip(tip)
        action.setStatusTip(tip)
    return action