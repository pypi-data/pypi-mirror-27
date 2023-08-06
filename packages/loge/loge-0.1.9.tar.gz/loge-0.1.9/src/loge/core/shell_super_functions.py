# -*- coding: utf-8 -*-
#--------------------------------------------------------------------
# Copyright (C) 2017, the Loge development team
#
# This file is part of Loge
# Loge is distributed under the terms of GNU General Public License
# The full license can be found in 'license.txt'
# Loge development team can be found in 'development.txt'
#--------------------------------------------------------------------


import re
import copy
import os

try:
    import svgwrite
except ImportError:
    pass
try:
    import matplotlib.pyplot as plt
except ImportError:
    pass
    
#----------------------------------------------

r_shell = None
variables = vars()

def vars_formated():
    out = copy.copy(variables)
    for key in out:
        if type(out[key]) is float:
            out[key] = round(out[key], r_shell.float_display_precison)
    return out

#----------------------------------------------

def r_comment(object):
    r_shell.report_markdown += str(object) + '\n\n'
    
def r_seepywarning(warning):
    r_comment('>>*!!! SeePyWarning - %s !!!*'%warning)

def r_mathcomment(object):
    comment_string = str(object)
    comment_string_formated = codeformat(comment_string)
    r_comment(comment_string_formated)
            
def r_adj(text = 'text', link = 'link', comment = 'somecomment', mode = 1, code = ''):
    islist = re.search(r'(\w+)\s*=\s*(\w+)\s*[[](\d+)[]]\s*', code)
    setvalues = None
    index = None
    #---changing True False display on report
    if text == 'True':
        text = '☑'
    if text == 'False':
        text = '☐'
    #---
    if islist:
        variable = islist.group(2)
        index = int(islist.group(3))
        setvalues = ('%(' + str(variable) + ')s') % vars_formated()
    if mode == 1:
        href='[{0}]({1};{3};{4}) {2}'.format(text, link, comment, setvalues, index)
    if mode == 2:
        href='{2} [{0}]({1};{3};{4})'.format(text, link, comment, setvalues, index)
    r_shell.report_markdown += href +'\n\n'
    
def r_img(imagename):
    image_path = os.path.dirname(r_shell.Script.script_path) + '/' + imagename
    r_shell.report_markdown += '![Alt text](%s)\n\n' % image_path

def r_plt(pltObject):
    try:
        name = str(r_shell._id) + '.png'
        image_path = r_shell.get_tmp_file_path(name)
        pltObject.savefig(image_path, dpi=(60))
        r_shell.report_markdown += '![Alt text](%s)\n\n' % image_path
        r_shell._id += 1
    except Exception as e :
        r_seepywarning('Matplotlib plt image save failure - %s' %str(e))
        
def r_pil(PilImageObject):
    try:
        name = str(r_shell._id)+ '.png'
        image_path = r_shell.get_tmp_file_path(name)
        PilImageObject.save(image_path)
        r_shell.report_markdown += '![Alt text](%s)\n\n' % image_path
        r_shell._id += 1
    except Exception as e :
        r_seepywarning('Pillow image save failure - %s' %str(e))
        
def r_tex(string):
    plt.figure(frameon=False)
    plt.axes(frameon=0)
    if string[0] != '$' and string[-1] != '$':
        string = '$' + string + '$'
    plt.text(0.0, 0.0, string, fontsize=600)
    plt.xticks(())
    plt.yticks(())
    plt.tight_layout()
    name = str(r_shell._id) + '.png'
    image_path = r_shell.get_tmp_file_path(name)
    plt.savefig(image_path, bbox_inches='tight', dpi=(2))
    plt.close()
    r_shell.report_markdown += '![Alt text](%s)\n\n' % image_path
    r_shell._id += 1

def r_codetex(string):
    r_tex(codeformat(string))

def r_svg(svgObject):
    name = str(r_shell._id) + '.svg'
    image_path = r_shell.get_tmp_file_path(name)
    if type(svgObject) in [str]:
        svg_file = open(image_path, "w")
        svg_file.write(svgObject)
        r_shell.report_markdown += '![Alt text](%s)\n\n' % image_path
        svg_file.close()
        r_shell._id += 1
    elif type(svgObject) is svgwrite.drawing.Drawing:
        svg_file = open(image_path, "w")
        svg_file.write(svgObject.tostring())
        r_shell.report_markdown += '![Alt text](%s)\n\n' % image_path
        svg_file.close()
        r_shell._id += 1
    else:
        r_seepywarning('Unknown SVG format given')

#----------

def codeformat(string):
    #changing 3**3 to 3^2
    string = string.replace('**', '^')
    #changing math.sin(1) to sin(1)
    string = string.replace('math.', '')
    #changing 3 * u.mm to 3[mm] - usable when Unum SI units system used in script
    string = re.sub(    r'\s*\*\s*u.(\w+)',
                        r'[\1]',
                        string  )
    #changing (3*u.mm + 3*u.m).asUnit(u.mm) to 3*u.mm + 3*u.m - usable when Unum SI units system used in script
    string = re.sub(    r'\((.+)\).asUnit\((.+)\)',
                        r'\1',
                        string  )            
    return string