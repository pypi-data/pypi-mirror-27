# -*- coding: utf-8 -*-
#--------------------------------------------------------------------
# Copyright (C) 2017, the Loge development team
#
# This file is part of Loge
# Loge is distributed under the terms of GNU General Public License
# The full license can be found in 'license.txt'
# Loge development team can be found in 'development.txt'
#--------------------------------------------------------------------
'''
---------------------------------------------------------------------
Toolbar module of a main window.
---------------------------------------------------------------------
'''

from PyQt5.QtWidgets import QToolBar, QCheckBox, QPushButton, QDoubleSpinBox, QRadioButton

from loge.gui.gui_utils import translate, TR_GUI_CONTEXT

class MainToolBar(QToolBar):

    def __init__(self,parent):
        super().__init__(translate(TR_GUI_CONTEXT,'Main'),parent)

    def add_toolbar_items(self,actions):
        if not actions:
            raise ValueError('An attribute "actions" dictionary can not be empty')
        if not isinstance(actions, dict):
            raise TypeError('An attribute "actions" should be a dictionary type')

        self.addAction(actions['file_new'])
        self.addAction(actions['file_open'])
        self.addAction(actions['file_save'])
        self.addSeparator()
        self.addAction(actions['reload_script_file'])
        self.watch_check_box = QCheckBox(translate(TR_GUI_CONTEXT,'watch script'))
        self.watch_check_box.setStatusTip(translate(TR_GUI_CONTEXT,'If active report will be reloaded after script file change'))
        self.addWidget(self.watch_check_box)
        self.addSeparator()
        self.addAction(actions['file_edit'])
        self.addSeparator()
        self.addAction(actions['print'])
        self.addAction(actions['save_markdown'])
        self.addSeparator()
        self.addAction(actions['show_source'])
        self.addAction(actions['show_html'])
        self.addAction(actions['show_markdown'])
        self.addAction(actions['show_loge'])
        self.addSeparator()
        self.addAction(actions['preview_markdown'])
        self.addSeparator()
        self.addAction(actions['syntax'])


class TimerToolBar(QToolBar):

    def __init__(self,parent):
        super().__init__(translate(TR_GUI_CONTEXT,'Timer'),parent)

    def add_toolbar_items(self):
        self.timerButton = QPushButton(translate(TR_GUI_CONTEXT,'Timer'), self)
        self.timerButton.setCheckable(True)
        self.timerButton.setStatusTip(translate(TR_GUI_CONTEXT,"If pushed timer active"))
        
        self.timerSpinBox = QDoubleSpinBox(self)
        self.timerSpinBox.setStatusTip(translate(TR_GUI_CONTEXT,"Time space in seconds"))
        self.timerSpinBox.setMinimum(0.1)
        self.timerSpinBox.setSingleStep(0.1)
        self.timerSpinBox.setValue(2.0)
        self.timerPulse = QRadioButton(self)
        self.timerPulse.setEnabled(False)

        self.addWidget(self.timerButton)
        self.addWidget(self.timerSpinBox)
        self.addWidget(self.timerPulse)
