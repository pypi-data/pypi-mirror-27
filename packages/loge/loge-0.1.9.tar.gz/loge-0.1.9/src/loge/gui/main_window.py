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
The module containing a main application window class.
---------------------------------------------------------------------
"""

from PyQt5.QtWidgets import QDesktopWidget, QMainWindow, QStyle
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtCore import Qt, QSize

from loge.gui.gui_utils import get_icon, create_action
from loge.gui.gui_utils import translate, TR_GUI_CONTEXT

# a scale of application window width to cover the % of the whole screen available space
_SW_WIDTH = 0.53 #53% because of width an image in start page
# a scale of application window height to cover the % of the whole screen available space
_SW_HEIGHT = 0.7
# application window minimum width in pixels
_MIN_W_WIDTH = 100
# application window minimum height in pixels
_MIN_W_HEIGHT = 100
# application logo icon
_APP_ICON = "logo.png"


class MainWindow(QMainWindow):

    def __init__(self,app_name,app_version):
        super().__init__()
        self.actions = {} #actions dictionary besides QWidget.actions() list
        self._init_main_window()
        self.main_title = app_name + ' (' + app_version+')'
        self.setWindowTitle(self.main_title)
        self._set_actions()


    def _init_main_window(self):
        # -- Window settings --
        ag = QDesktopWidget().availableGeometry()
        window_size = ag.size()
        app_width = _SW_WIDTH * window_size.width()
        app_height = _SW_HEIGHT * window_size.height()
        window_size.scale(app_width,app_height,Qt.IgnoreAspectRatio)
        self.setGeometry(
        QStyle.alignedRect(Qt.LeftToRight,
            Qt.AlignCenter,
            window_size,
            ag
        ))
        self.setMinimumSize(_MIN_W_WIDTH,_MIN_W_HEIGHT)
        self.setWindowIcon(get_icon(_APP_ICON))

    def _set_actions(self):
        self.actions['file_new'] = create_action('new.png','New',QKeySequence.New
                            ,'Create new *.py script from template',self)

        self.actions['file_open'] = create_action('open.png','Open',QKeySequence.Open
                              ,'Open existing *.py script',self)
        
        self.actions['file_openreadonly'] = create_action('openreadonly.png','Open read only'
                                      ,None,'Open existing *.py script - edit and saving not aloved',self)
        
        self.actions['file_save'] = create_action('save.png','Save',QKeySequence.Save
                               ,'Save changes to script file',self)

        self.actions['file_saveas'] = create_action('saveas.png','Save as',QKeySequence.SaveAs
                                 ,'Save current script',self)

        self.actions['reload_script_file'] = create_action('reload.png','Reload',QKeySequence.Refresh
                                 ,'Reload *.py script',self)

        self.actions['file_edit'] = create_action('edit.png','Edit','Ctrl+E'
                              ,'It opens to edit current *.py script',self)

        self.actions['show_html'] = create_action('showhtml.png','Show report as HTML',None
                                  ,'It shows report as HTML code',self)

        self.actions['show_markdown'] = create_action('showmarkdown.png','Show report as Markdown',None
                                     ,'It shows report as Markdown code',self)

        self.actions['show_source'] = create_action('showsource.png','Show python source',None
                                    ,'It shows python source code',self)

        self.actions['show_loge'] = create_action('showreport.png','Back to Loge report',None
                                   ,'Back to Loge report',self)

        self.actions['preview_markdown'] = create_action('previewmarkdown.png','Preview some Markdown',None
                                   ,'You can preview some Markdown document - it not change watched *.py script',self)

        self.actions['save_markdown'] = create_action('savemarkdown.png','Save report as Markdown file',None
                                   ,'Save raport as Markdown file',self)
#
#        #savemarkdownAction = QAction(QIcon(get_icon_path("savemarkdown.png")),"Save report as Markdown file",self)
#        #savemarkdownAction.setStatusTip("Save report as Markdown file")
#        #savemarkdownAction.triggered.connect(self.SaveMarkdown)
#
#        #printAction = QAction(QIcon(get_icon_path("print.png")),"Print document",self)
#        #printAction.setStatusTip("Print document")
#        #printAction.setShortcut("Ctrl+P")
#        #printAction.triggered.connect(self.Print)
        self.actions['print'] = create_action('print.png',translate(TR_GUI_CONTEXT,'Print document'),QKeySequence.Print
                               ,translate(TR_GUI_CONTEXT,'Print document'),self)

        self.actions['help'] = create_action('help.png',translate(TR_GUI_CONTEXT,'Help'),QKeySequence.HelpContents
                              ,translate(TR_GUI_CONTEXT,'Help information'),self)

        self.actions['about'] = create_action('about.png',translate(TR_GUI_CONTEXT,'About')
                               ,None,translate(TR_GUI_CONTEXT,'Loge project information'),self)

        self.actions['floatprecision'] = create_action(None,translate(TR_GUI_CONTEXT,'Float precision'),None
                                        ,translate(TR_GUI_CONTEXT,'Set float display precision'),self)

        self.actions['syntax'] = create_action('syntax.png',translate(TR_GUI_CONTEXT,'Syntax help'),'F2'
                                ,translate(TR_GUI_CONTEXT,'Show Loge syntax help'),self)

        self.actions['tutorial'] = create_action('tutorial.png',translate(TR_GUI_CONTEXT,'Tutorial'),None
                                  ,translate(TR_GUI_CONTEXT,'Open tutorial script'),self)        

    def set_action_slot(self,action_name,slot):
        """
        Sets a slot to an action.

        Args:
            action_name (str): the name of an action
            slot: a function that is called in response to a signal
        """
        self.actions[action_name].triggered.connect(slot)
