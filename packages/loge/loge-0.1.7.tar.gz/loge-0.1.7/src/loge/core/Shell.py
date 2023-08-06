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
import sys
import re
import copy
import tempfile

from PyQt5.QtWidgets import QFileDialog

from loge.core.core_utils import get_html_from_markdown


import loge.core.shell_super_functions as super_functions



class Shell():
    def __init__(self):
        self.report_markdown = ''
        self.report_html = ''
        #---
        self.savedir = os.path.dirname(__file__)
        #---
        self.Script = None
        #----
        self.tmpdir = None
        self.create_tempdir()
        #----
        self.tempfile_nameprefix = 'tmp_loge_'
        #----
        self.float_display_precison = 3

    #------------------------
        
    def assign_code(self, CodeObiect):
        self.Script = CodeObiect

    #------------------------
    
    def create_tempdir(self):
        if not self.tmpdir:
            dirpath = tempfile.mkdtemp()
            dirname = os.path.basename(dirpath)
            new_dirname = 'loge_' + dirname
            new_dirpath = dirpath.replace(dirname, new_dirname)
            os.rename(dirpath, new_dirpath)
            self.tmpdir = new_dirpath

    def get_tmp_file_path(self, filename):
        filename = self.tempfile_nameprefix + filename # adding prefix to name
        tmp_file_path = os.path.join(self.tmpdir, filename)
        return tmp_file_path

    #------------------------

    def run_oryginal(self):
        exec (self.Script.code_oryginal in globals(), locals())

    def run_parsed(self):
        self.report_markdown = ''
        self.report_html = ''
        self._id = 1
        #-----------------------------------------------------------------
        # Here are functions needed in namespace where parsed code is run
        #-----------------------------------------------------------------
        super_functions.r_shell = self
        super_functions.variables = vars()        
        #--------
        r_comment = super_functions.r_comment
        r_seepywarning = super_functions.r_seepywarning
        r_mathcomment = super_functions.r_mathcomment
        r_adj = super_functions.r_adj
        r_img = super_functions.r_img
        r_plt = super_functions.r_plt           
        r_pil = super_functions.r_pil
        r_tex = super_functions.r_tex
        r_codetex = super_functions.r_codetex
        codeformat = super_functions.codeformat
        r_svg = super_functions.r_svg
        vars_formated = super_functions.vars_formated
        #---Adding current script dir to python PATH list
        #---(user will be able to import modules from dir where his seepy script is stored)
        script_dir = os.path.dirname(self.Script.script_path)
        sys.path.append(script_dir) 
        #-----------------------------------------------------------------
        #---------- Here the code_parsed is finally executed -------------
        #-----------------------------------------------------------------
        exec(self.Script.code_parsed)
        #-----------------------------------------------------------------
        #-----------------------------------------------------------------
        #---so the report_markdown has been created-----------------------
        #---and mistune is used to get report_html from report_markdown
        self.report_html = get_html_from_markdown(self.report_markdown)
        #-----------------------------------------------------------------
        self._id = 0
        #---Deleting current script dir from python PATH list
        sys.path = list(set(sys.path)) # first deleting duplicates
        sys.path.remove(script_dir) # and finaly deleting script dir 

    #------------------------
    
    def __del__ (self):
        if self.tmpdir:
            self.close_shell()
        
    def close_shell (self):
        self.delete_tmpfile(deleteall=True)
        os.removedirs(self.tmpdir)
        self.tmpdir = None
            
    def delete_tmpfile(self, deleteall=False):
        if deleteall:
            for content in os.listdir(self.tmpdir):
                os.remove(self.tmpdir + '/' + content)
        else:
            for content in os.listdir(self.tmpdir):
                if self.tempfile_nameprefix in content :
                    os.remove(self.tmpdir + '/' + content)
            
    #------------------------
    
    def save_report_markdown(self, savedir = os.path.dirname(__file__), initfilename = 'new.md'):
        #---asking for file path
        filename = QFileDialog.getSaveFileName(caption = 'Save as Markdown document',
                                                directory = self.savedir + '/' + initfilename,
                                                filter = "Markdown document (*.md)")[0]
        filename = str(filename)
        #---
        if not filename == '':
            self.savedir = os.path.dirname(filename)
            md_file = open(filename, "w")
            md_file.write(self.report_markdown)
            md_file.close()