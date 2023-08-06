# -*- coding: utf-8 -*-
#--------------------------------------------------------------------
# Copyright (C) 2017, the Loge development team
#
# This file is part of Loge
# Loge is distributed under the terms of GNU General Public License
# The full license can be found in 'license.txt'
# Loge development team can be found in 'development.txt'
#--------------------------------------------------------------------

import os
import re
import shutil

import codecs

from PyQt5.QtWidgets import QFileDialog, QInputDialog, QMessageBox, QLineEdit

from loge.memos import appinfo
from loge.core.core_utils import APP_PATH
from loge.core import script_parsing as script_parsing

class Script():
    
    def __init__(self):
        #---
        self._script_path = ''
        self._script_path_observers = []
        self.savedir = APP_PATH
        #---
        self.code_oryginal = ''
        self.code_parsed = ''
        #---
        self.stamptext = appinfo.report_stamp
        #--
        self.saveLock = False
        #--
        self.watcher = None
        self._watcher_active = False

    #------------------------
    
    @property 
    def script_path(self):
        return self._script_path

    @script_path.setter
    def script_path(self,value):
        self._script_path = value
        if self._watcher_active: #if checkbox checked (watcher active) activate it for new path
            self.activate_watcher()

    #------------------------

    def set_watcher(self, watcher):
        self.watcher = watcher

    def activate_watcher(self):
        #print('watcher script path: '+self.script_path)
        if self.watcher and self.script_path != '':
            #print('dodaje sciezke: '+self.script_path)
            self.deactivate_watcher() #clear current watcher's paths
            if self.watcher.addPath(self.script_path):
                #print('sciezka dodana '+ str(self.watcher.files()))
                pass
            else:
                #print('sciezka nie dodana')
                pass
        self._watcher_active = True

    def deactivate_watcher(self):
        if self.watcher and self.script_path != '':
            #clear watcher paths
            if self.watcher.files():
                self.watcher.removePaths(self.watcher.files())
        self._watcher_active = False

    #------------------------

    def parse(self):
        script = self.code_oryginal
        #--parsing extra loge command syntax
        script = script_parsing.parse(script)
        #--report end stamp
        script += "\nr_comment('>>*----- %s -----*')"%self.stamptext
        #--saving
        self.code_parsed = script 

    #------------------------

    def editCode(self, lineID = 'id1', setvalues = None, index = None):
        if setvalues == 'None':
            setvalues = None
        #---
        script = self.code_oryginal
        #---
        script = re.sub(r'#(<{2,})', r"#\1_idx_", script)
        no = 1  
        while re.search(r"#<{2,}_idx_", script):
            script = script.replace(r'<_idx_', r"<_id%s_" % no, 1)
            no += 1 
        #---OPTION 1 Selectind one form list if list
        if setvalues :
            setvalues = re.search(r'[[](.+)[]]', setvalues).group(1)
            setvalues = setvalues.replace(" ", "")
            setvalues = setvalues.replace("'", "")
            setvalues = setvalues.split(',')
            #---
            expresion = re.search(r'(\w+)\s*=\s*(\w+)\s*[[](\d+)[]]\s*#<{2,}_%s_'%lineID, script)
            variable = expresion.group(1)
            listindex = int(expresion.group(3))
            #---asking for new value from choice list
            value_selected = QInputDialog.getItem(None, 'Set new value', variable +'=', setvalues, listindex, False)[0]
            #---
            if value_selected:
                index_selected = setvalues.index(value_selected)
            else:
                index_selected = listindex
            #---
            script = re.sub(    r'(\w+)\s*=\s*(.+)[[]\w+[]]\s*#(<{2,})_%s_'%lineID,
                                r'\1 = \2[%s] #\3_%s_'%(index_selected, lineID),
                                script  )
        #---OPTION 2 Geting new variable value   
        else:
            expresion = re.search(r'(\w+)\s*=\s*(.+)\s*#<{2,}_%s_'%lineID, script)
            variable = expresion.group(1)
            oldvalue = expresion.group(2)
            oldvalue = oldvalue.rstrip() #for now this hotfix delete whitespace from the end of oldvalue string
            newvalue = None
            #---asking for new value
            if ('filepath' in variable): # if variable look like filepath
                directory = '/'
                try:
                    if os.path.isdir(os.path.dirname(eval(oldvalue))):
                        directory = os.path.dirname(eval(oldvalue))
                except:
                    pass
                askmsg = "Select new filepath for '%s' variable" %variable
                filename = QFileDialog.getOpenFileName(caption=askmsg, directory=directory)[0]
                if filename == '':
                    newvalue = oldvalue
                else:
                    newvalue = "'%s'"%str(filename)
            elif ('dirpath' in variable): # if variable look like dirpath
                directory = '/'
                try:
                    if os.path.isdir(eval(oldvalue)):
                        directory = os.path.dirname(eval(oldvalue))
                except:
                    pass
                dirname = QFileDialog.getExistingDirectory(caption = 'Select directory', directory = directory)
                if dirname == '':
                    newvalue = oldvalue
                else:                
                    newvalue = "'%s'"%str(dirname)
            elif (oldvalue.strip() in ['True', 'False']): # if variable has bool value
                bool_oldvalue = eval(oldvalue)
                newvalue = str(not(bool_oldvalue))
            else: # other cases
                input_result = QInputDialog.getText(None, 'Set new value',variable +'=', QLineEdit.Normal,oldvalue)
                if input_result[1]:
                    newvalue = input_result[0]

            #---
            if newvalue:
                script = re.sub(r'(\w+)\s*=\s*(.+)\s*#(<{2,})_%s_'%lineID,
                                r'\1 = %s #\3_%s_'%(newvalue, lineID),
                                script  )
        #---
        script = re.sub(r"#(<{2,})_id(\d+)_", r'#\1', script)
        #---
        self.code_oryginal = script

    #------------------------        

    def getTimerParameters(self):
        is_active = False
        timespace = None
        #---
        script = self.code_oryginal
        timer = re.search(r"#%timer[ ]*(\d*)[ ]*ON", script)
        if timer:
            is_active = True
            timespace  = float(timer.group(1)) / 1000
            return is_active, timespace
        timer = re.search(r"#%timer[ ]*(\d*)[ ]*OFF", script)
        if timer:
            is_active = False
            timespace  = float(timer.group(1)) / 1000
            return is_active, timespace
        return None
        
    #------------------------ 

    def savecode(self):
        if self.saveLock:
            QMessageBox.information(None, 'Info', 'File open read only. Use save as option')
            return False
        else:
            file = codecs.open(self.script_path,'r+', 'utf-8')
            file.write(self.code_oryginal)
            file.close()
            return True

    def openFile(self, file_path=None, saveLock = False):
        #---asking for file path if not given
        if file_path:
            filename =  file_path
        else:
            filename = QFileDialog.getOpenFileName(caption = 'Open script',
                                                    directory = self.savedir,
                                                    filter = "Python script (*.py)")
            filename = str(filename[0])
        #---
        if not filename == '':
            self.savedir = os.path.dirname(filename)
            self.script_path = filename
            file = codecs.open(self.script_path, 'r', 'utf-8')
            self.code_oryginal = file.read()    
            file.close()      
            self.parse()
            self.saveLock = saveLock
        else:
            pass
    
    def open_markdown(self):
        filename = QFileDialog.getOpenFileName(caption = 'Open Markdown document',
                                                directory = self.savedir,
                                                filter = "Markdown document (*.md)")
        filename = str(filename[0])
        return filename

    def newFile(self, template_path, info='Save as', initfilename='your_script', filedirectory = None):
        #---asking for file path
        if filedirectory is None:
            filename,ffilter = QFileDialog.getSaveFileName(caption = info,
                                                    directory = self.savedir + '/' + initfilename,
                                                    filter = "Python script (*.py)")
        else:
            filename = filedirectory + '/' + initfilename
        #---
        if not filename == '':
            new_template = codecs.open(template_path,'r', 'utf-8').read()
            self.savedir = os.path.dirname(filename)
            text_file = codecs.open(filename, 'w', 'utf-8')
            text_file.write(new_template)
            text_file.close()
            self.script_path = filename
            self.reloadcode()
            self.parse()
            self.saveLock = False

    def saveAs(self, savepath = None):
        newname = 'Copy_' + os.path.basename(self.script_path)
        #---asking for file path
        initdir = self.savedir + '/' + newname
        if self.saveLock:
            initdir = '/' + newname
        if savepath:
            filename = savepath
        else:
            filename = QFileDialog.getSaveFileName(caption = 'Save as',
                                                        directory = initdir,
                                                        filter = "Python script (*.py)")[0]
            filename = str(filename)
        #---
        new_file = codecs.open(filename,'w', 'utf-8')
        new_file.write(self.code_oryginal)
        new_file.close()
        #---coping files linked inside code_oryginal
        src_dir = os.path.dirname(self.script_path)
        dst_dir = os.path.dirname(filename)
        copied_dependences = []
        for fname in os.listdir(src_dir):   
            if  fname in self.code_oryginal:
                scr_file = os.path.join(src_dir, fname)
                dst_file = os.path.join(dst_dir, fname)
                if not scr_file == dst_file:
                    if os.path.isfile(scr_file) and ('.' in scr_file):
                        shutil.copyfile(scr_file, dst_file)
                        copied_dependences.append(fname)
        #---
        self.script_path = filename
        self.savedir = os.path.dirname(filename)
        self.reloadcode()
        self.parse()
        self.saveLock = False
        #---info massage
        infotext = 'Saved to '+ filename + '\n'
        if not copied_dependences == []:
            infotext += 'Copied_dependences: \n' 
            for i in copied_dependences:
                infotext += str(i) + '\n' 
        QMessageBox.information(None, 'Info', infotext)

    def reloadcode(self):
        file = codecs.open(self.script_path,'r', 'utf-8')
        self.code_oryginal = file.read()    
        file.close()