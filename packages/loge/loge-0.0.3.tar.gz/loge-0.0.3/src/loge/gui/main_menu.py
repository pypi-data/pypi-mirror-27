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
Menu bar module of a main window.
---------------------------------------------------------------------
'''

from PyQt5.QtWidgets import QMenuBar

from loge.gui.gui_utils import translate, TR_GUI_CONTEXT

class MainMenuBar(QMenuBar):

    def __init__(self,parent):
        super().__init__(parent)
        self._init_menu_bar()

    def _init_menu_bar(self):
        self.m_file = self.addMenu(translate(TR_GUI_CONTEXT,"&File"))
        self.m_script = self.addMenu(translate(TR_GUI_CONTEXT,"&Script"))
        self.m_help = self.addMenu(translate(TR_GUI_CONTEXT,"&Help"))


    def add_menu_items(self,actions):
        if not actions:
            raise ValueError('An attribute "actions" dictionary can not be empty')
        if not isinstance(actions, dict):
            raise TypeError('An attribute "actions" should be a dictionary type')

        self.m_file.addAction(actions['file_new'])
        self.m_file.addAction(actions['file_open'])
        self.m_file.addAction(actions['file_openreadonly'])
        self.m_file.addSeparator()
        self.m_file.addAction(actions['file_save'])
        self.m_file.addAction(actions['file_saveas'])
        self.m_file.addSeparator()
        self.m_file.addAction(actions['print'])

        self.m_script.addAction(actions['reload_script_file'])
        self.m_script.addAction(actions['file_edit'])
        self.m_script.addAction(actions['show_html'])
        self.m_script.addAction(actions['show_markdown'])
        self.m_script.addAction(actions['show_loge'])
        self.m_script.addAction(actions['floatprecision'])

        self.m_help.addAction(actions['help'])
        self.m_help.addAction(actions['syntax'])
        self.m_help.addAction(actions['tutorial'])
        self.m_help.addSeparator()
        self.m_help.addAction(actions['about'])