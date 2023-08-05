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
Extra module used for code refactoring.
This is a temporary container for procedures, classes etc.
that are moved from other modules during code refactoring.
If needed they should be refactored and should be moved
to more suitable module or class.
---------------------------------------------------------------------
'''

import os
import re

import mistune

def abspath(relpath=None):
    _this_dir = os.path.dirname(os.path.abspath(__file__))
    _loge_dir = os.path.split(_this_dir)[0]
    if relpath:
        return os.path.join(_loge_dir, relpath)
    else:
        return _loge_dir
APP_PATH = abspath()

def get_html_from_markdown(markdown='#*test*'):
    html = mistune.markdown(markdown)
    return html

def get_html_from_markdownfile(markdown_abspath):
    memo_page = open(markdown_abspath, 'r').read()
    #---replaceing path to images inside markdown
    img_dir =  os.path.split(markdown_abspath)[0]
    markdown = re.sub(  r'!\[(.+)\]\((.+)\)', 
                        r"![\1]({0}/\2)".format(img_dir), 
                        memo_page)
    #---
    html_page = get_html_from_markdown(markdown)
    return html_page

def get_html_from_memo(markdown_memo='x_help.md'):
    meno_abspath = abspath('memos/' + markdown_memo)
    html_page = get_html_from_markdownfile(meno_abspath)
    return html_page

def get_html_from_code(code='a=1'):
    markdown_page = "````\n" + code + "\n````"
    html_page = get_html_from_markdown(markdown_page)
    return html_page
