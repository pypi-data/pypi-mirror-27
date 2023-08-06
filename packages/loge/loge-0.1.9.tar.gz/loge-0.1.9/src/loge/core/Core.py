# -*- coding: utf-8 -*-
#--------------------------------------------------------------------
# Copyright (C) 2017, the Loge development team
#
# This file is part of Loge
# Loge is distributed under the terms of GNU General Public License
# The full license can be found in 'license.txt'
# Loge development team can be found in 'development.txt'
#--------------------------------------------------------------------

import subprocess
import idlelib
import traceback
import os
#import codecs
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMessageBox, QDialog, QInputDialog
from PyQt5.QtPrintSupport import QPrintDialog
from PyQt5.QtGui import QCursor

from loge.core.Script import Script
from loge.core.Shell import Shell

from loge.core.core_utils import abspath, get_html_from_memo, get_html_from_code, get_html_from_markdownfile

class Core():
    
    def __init__(self):
        self.Script = Script()
        self.Shell = Shell()
        self.Gui = None
        #---
        self.watcher = None
        self.timer = None
        #---
        self.set_watcher()
        self.set_timer()
        self.Shell.assign_code(self.Script)

    def set_watcher(self):
        self.watcher = QtCore.QFileSystemWatcher()
        self.watcher.fileChanged.connect(self.script_changed)
        self.Script.set_watcher(self.watcher)

    def set_timer(self):
        # -- Timer --
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.TimerAction)

    def watcher_clicked(self,checked):
        if checked:
            self.Script.activate_watcher()
        else:
            self.Script.deactivate_watcher()

    def script_changed(self,file):
        self.Script.reloadcode()
        self.refresh()

    #------------------------ 

    def refresh(self, waitcursor = True):
        successruned = False
        #some OS updating file first save 0 bits than save right size
        #because of that set scrollBar doesn't work
        #we don't want reload browser if file size is zero 
        file_info = QtCore.QFileInfo(self.Script.script_path)
        if 0 == file_info.size():
            return successruned
        message = None
        error_trace = None
        if waitcursor:
            QApplication.setOverrideCursor(QCursor(QtCore.Qt.WaitCursor))
        try:
            self.Script.parse()
            self.Shell.run_parsed()
            self.Gui.browser_reload(self.Shell.report_html)
            successruned = True
        except Exception as e:
            message = 'Some problem - ' + str(e)
            error_trace = str(traceback.format_exc())
        finally:
            QApplication.restoreOverrideCursor()
        
        if not successruned and message:
            QMessageBox.information(None, message, error_trace)
        #---
        apptitle = ' - ' + os.path.basename(self.Script.script_path)
        if self.Script.saveLock:
            apptitle += '  (read only)'
        apptitle = self.Gui.get_app_main_title() + apptitle
        self.Gui.set_app_title(apptitle)
        #---
        return successruned

    def reload_script_file(self):
        if self.Script.script_path :
            self.Script.reloadcode()
            self.refresh()
        else:
            QMessageBox.information(None, 'Info', 'Please create or open script first')

    #------------------------ 

    def file_new(self):
        template_path = abspath('templates/x_newtemplate.py')
        self.Script.newFile(template_path, 'Save new script as', 'newScript.py')
        self.refresh()
            
    def file_open(self, file_path = None, saveLock = False):
        self.Shell.delete_tmpfile() #Cleaning Loge tmp files
        self.Script.openFile(file_path, saveLock)
        self.refresh()
        #--Timer
        self.TimerFromCode()

    def file_openreadonly(self, file_path = None):
        self.file_open(file_path = None, saveLock = True)

    def file_save(self):
        if self.Script.script_path :
            if self.Script.savecode():
                QMessageBox.information(None, 'Info', 'Saved to '+ self.Script.script_path)
        else:
            QMessageBox.information(None, 'Info', 'Please create or open script first')

    def file_saveas(self):
        if self.Script.script_path :
            self.Script.saveAs()
            self.refresh()
        else:
            QMessageBox.information(None, 'Info', 'Please create or open script first')

    def file_edit(self):
        if self.Script.saveLock:
            QMessageBox.information(None, 'Info', 'File open read only. Use save as option')
            return False
        if self.Script.script_path :
            subprocess.Popen(['python', '-m', 'idlelib.idle', self.Script.script_path]) 
        else:
            QMessageBox.information(None, 'Info', 'Please create or open script first')

    #------------------------ 

    def show_python_source(self):
        if self.Script.script_path :
            html_page = get_html_from_code(self.Script.code_oryginal)
            self.Gui.set_browser_content(html_page)
        else:
            QMessageBox.information(None, 'Info', 'Please create or open script first')

    def show_html(self):
        if self.Script.script_path :
            html_page = get_html_from_code(self.Shell.report_html)
            self.Gui.set_browser_content(html_page)
        else:
            QMessageBox.information(None, 'Info', 'Please create or open script first')

    def show_markdown(self):
        if self.Script.script_path:
            html_page = get_html_from_code(self.Shell.report_markdown)
            self.Gui.set_browser_content(html_page)
        else:
            QMessageBox.information(None, 'Info', 'Please create or open script first')

    def show_loge(self):
        if self.Script.script_path :
            self.Gui.set_browser_content(self.Shell.report_html)
        else:
            QMessageBox.information(None, 'Info', 'Please create or open script first')

    def show_syntax(self):
        html_page = get_html_from_memo('x_syntax.md')
        self.Gui.set_browser_content(html_page)

    #------------------------
    def PreviewMarkdown(self):
        #---asking for file path
        filename = self.Script.open_markdown()
        if not filename == '':
            #---
            #show_markdown_file(filename)
            html_page = get_html_from_markdownfile(filename)
            self.Gui.set_browser_content(html_page)

    def SaveMarkdown(self):
        if self.Script.script_path :
            initname = os.path.basename(self.Script.script_path).replace('.py', '.md')
            self.Shell.save_report_markdown(self.Script.savedir, initname)
        else:
            QMessageBox.information(None, 'Info', 'Please create or open script first')

    #------------------------ 
            
    def startpage(self):
        html_page = get_html_from_memo('x_startpage.md')
        self.Gui.set_browser_content(html_page)

    def help(self):
        html_page = get_html_from_memo('x_help.md')
        self.Gui.set_browser_content(html_page)

    def about(self):
        html_page = get_html_from_memo('x_about.md')
        self.Gui.set_browser_content(html_page)

    #------------------------ 

    def file_print(self):
        dialog = QPrintDialog()
        if dialog.exec_() == QDialog.Accepted:
            self.Gui.get_browser_document().print_(dialog.printer())
    
    #------------------------ 

    def tutorial(self):
        tutorial_path = abspath('memos/x_tutorial.py')
        savedir = self.Script.savedir #coping current savedir
        #--opening oryginal tutorial
        self.Shell.delete_tmpfile()
        self.Script.openFile(tutorial_path)
        #---saving temporary tutorial copy
        tutorial_tmppath = os.path.join(self.Shell.tmpdir, 'tmp_tutorial.py')
        self.Script.saveAs(tutorial_tmppath)
        #---opening temporary tutorial copy
        self.Shell.delete_tmpfile()
        self.Script.openFile(tutorial_tmppath)
        self.Script.savedir = savedir #back to previouse savedir
        self.refresh()
        self.file_edit()

    #------------------------ 

    def floatprecision(self):
        if self.Script.script_path :
            #---asking for precision as int number
            value = QInputDialog.getInt(    None, 
                                            'Float display precysion', 'Set the precison:',
                                            value = self.Shell.float_display_precison,
                                            min = 1, max = 9, step = 1)[0]
            #---
            self.Shell.float_display_precison = value
            self.refresh()
        else:
            QMessageBox.information(None, 'Info', 'Please create or open script first')

    #-----------------------

    def TimerButtonClicked(self):
        if self.Script.script_path:
            if self.Gui.toolbar_timer.timerButton.isChecked():
                self.TimerStart()
            if not self.Gui.toolbar_timer.timerButton.isChecked():
                self.TimerStop()
        else:
            self.TimerStop()
            QMessageBox.information(None, 'Info', 'Please create or open script first')

    def TimerAction(self):
        if self.Script.script_path:
            if self.Gui.toolbar_timer.timerButton.isChecked():
                self.Gui.toolbar_timer.timerPulse.setChecked(not(self.Gui.toolbar_timer.timerPulse.isChecked()))
                self.refresh(False)

    #---------------------
    def TimerStart(self):
        timespace = int(self.Gui.toolbar_timer.timerSpinBox.value() * 1000)
        self.timer.start(timespace)
        self.Gui.toolbar_timer.timerButton.setChecked(True)
        self.Gui.toolbar_timer.timerSpinBox.setEnabled(False)
        self.Gui.toolbar_timer.timerPulse.setEnabled(True)
        self.refresh(False)
                
    def TimerStop(self):
        self.timer.stop()
        self.Gui.toolbar_timer.timerButton.setChecked(False)
        self.Gui.toolbar_timer.timerSpinBox.setEnabled(True)
        self.Gui.toolbar_timer.timerPulse.setChecked(False)
        self.Gui.toolbar_timer.timerPulse.setEnabled(False)

    def TimerFromCode(self):
        parameters = self.Script.getTimerParameters()
        if parameters:
            self.Gui.toolbar_timer.timerButton.setChecked(parameters[0])
            self.Gui.toolbar_timer.timerSpinBox.setValue(parameters[1])
            if parameters[0]:
                self.TimerStart()
        else:
            self.TimerStop()
            self.Gui.toolbar_timer.timerButton.setChecked(False)
            self.Gui.toolbar_timer.timerSpinBox.setValue(2.0)
