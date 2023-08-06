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
--------------------------------------------------------------------------
GUI
--------------------------------------------------------------------------
'''

from loge.gui.main_window import MainWindow
from loge.gui.browser import Browser
from loge.gui.main_menu import MainMenuBar
from loge.gui.main_toolbar import MainToolBar, TimerToolBar

class Gui():

    def __init__(self, app_name, app_version):
        self.Core = None
        #---
        self.main_window = MainWindow(app_name, app_version)
        # -- Menubar --
        self.menu_bar = MainMenuBar(self.main_window)
        self.menu_bar.add_menu_items(self.main_window.actions)
        self.main_window.setMenuBar(self.menu_bar)
        # -- Toolbars --
        # -- MainToolbar
        self.toolbar = MainToolBar(self.main_window)
        self.toolbar.add_toolbar_items(self.main_window.actions)
        self.main_window.addToolBar(self.toolbar)
        # -- TimerToolbar
        self.toolbar_timer = TimerToolBar(self.main_window)
        self.toolbar_timer.add_toolbar_items()
        self.toolbar_timer.setVisible(False)
        self.main_window.addToolBar(self.toolbar_timer)
        # -- Text Browser as Central Widget --
        self.browser = Browser()
        self.main_window.setCentralWidget(self.browser)
        self.browser.setOpenLinks(False)
        self.browser.anchorClicked.connect(self.on_anchor_clicked)
        # -- Statusbar --
        self.status_bar = self.main_window.statusBar()
    
    def connect_to_core(self, Core):
        self.Core = Core
        self._set_actions_slots()
        self._set_watch_slot()
        self._set_timer_slot()
        #---
        Core.Gui = self
        #---
        self.Core.startpage()

    def _set_actions_slots(self):
        self.main_window.set_action_slot('file_new', self.Core.file_new)
        self.main_window.set_action_slot('file_open', self.Core.file_open)
        self.main_window.set_action_slot('file_openreadonly', self.Core.file_openreadonly)
        self.main_window.set_action_slot('file_save', self.Core.file_save)
        self.main_window.set_action_slot('file_saveas', self.Core.file_saveas)
        self.main_window.set_action_slot('file_edit', self.Core.file_edit)
        self.main_window.set_action_slot('reload_script_file', self.Core.reload_script_file)
        self.main_window.set_action_slot('print', self.Core.file_print)
        self.main_window.set_action_slot('show_source', self.Core.show_python_source)
        self.main_window.set_action_slot('show_html', self.Core.show_html)
        self.main_window.set_action_slot('show_markdown', self.Core.show_markdown)
        self.main_window.set_action_slot('show_loge', self.Core.show_loge)
        self.main_window.set_action_slot('preview_markdown', self.Core.PreviewMarkdown)
        self.main_window.set_action_slot('save_markdown', self.Core.SaveMarkdown)
        self.main_window.set_action_slot('syntax', self.Core.show_syntax)
        self.main_window.set_action_slot('floatprecision', self.Core.floatprecision)
        self.main_window.set_action_slot('help', self.Core.help)
        self.main_window.set_action_slot('about', self.Core.about)
        self.main_window.set_action_slot('tutorial', self.Core.tutorial)

    def _set_watch_slot(self):
        """
        Sets a slot to an action of toolbar's watch script checkbox
        """
        self.toolbar.watch_check_box.clicked.connect(self.Core.watcher_clicked)

    def _set_timer_slot(self):
        """
        Sets a slot to an action of Timer button of Timer toolbar
        """
        self.toolbar_timer.timerButton.clicked.connect(self.Core.TimerButtonClicked) 

    def browser_reload(self,content):
        scroll_value = self.browser.verticalScrollBar().value()
        self.set_browser_content(content)
        self.browser.verticalScrollBar().setValue(scroll_value)

    def set_browser_content(self, content):
        self.browser.clear()
        self.browser.setHtml(content)

    def get_browser_document(self):
        return self.browser.document()

    def show(self):
        self.main_window.show()

    def get_app_main_title(self):
        return self.main_window.main_title

    def get_app_title(self):
        return self.main_window.windowTitle()

    def set_app_title(self,title):
        self.main_window.setWindowTitle(title)

    def on_anchor_clicked(self,url):
        link = str(url.toString())
        line_id = link.split(';')[0]
        setvalues = link.split(';')[1]
        index = link.split(';')[2]
        tmp = self.Core.Script.code_oryginal
        self.Core.Script.editCode(line_id, setvalues, index)
        if self.Core.refresh():
            pass
        else:
            self.Core.Script.code_oryginal = tmp

    def closeEvent(self, event):
        self.Core.Shell.close_shell()
        event.accept()