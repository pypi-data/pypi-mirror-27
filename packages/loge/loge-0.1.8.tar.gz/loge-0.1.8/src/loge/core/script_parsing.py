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

def parse(script=''):
    #-------------------------------------------------------------------------
    #Here the code_oryginal is changed in to code_parsed with re.sub() replace
    #-------------------------------------------------------------------------
    
    script = re.sub(r'\r\n', r'\n', script) #new line \n (Linux) vs \r\n (windows) problem
    
    #--Variable with one line comment syntax (indentation acceptable)
    script = re.sub(    r'([ \t]*)(\w+)(.+)#!(.*)',
                        r"\1\2\3 \n\1r_comment('''```\2 = %(\2)s``` \4''' % vars_formated())",
                        script  )
                        
    #--Result EQUation  with one line comment syntax, version /a = d + 4 = 5/ (indentation acceptable)
    script = re.sub(    r'([ \t]*)(\w+)\s*=\s*(.+)#%requ(.*)',
                        r"\1\2 = \3 \n\1r_mathcomment('''```\2 = \3 = %(\2)s``` \4''' % vars_formated())",
                        script  )
                        
                        
    #--EQUation with one line comment syntax, version /a = d + 4/ (indentation acceptable)
    script = re.sub(    r'([ \t]*)(\w+)\s*=\s*(.+)#%equ(.*)',
                        r"\1\2 = \3 \n\1r_mathcomment('''```\2 = \3``` \4''' % vars_formated())",
                        script  )
                        
    #--Result EQUation with one line comment syntax, version /d + 4 = 5/ (indentation acceptable)
    script = re.sub(    r'([ \t]*)(\S[^=\^\n]+)#%requ(.*)',
                        r"\1\2 \n\1r_tmp =  \2 \n\1r_mathcomment('''```\2 = %(r_tmp)s``` \3'''.format(\2) % vars_formated()) \n\1r_tmp =  None",
                        script  )
                        
    #--EQUation with one line comment syntax, version /d + 4/  (indentation acceptable)
    script = re.sub(    r'([ \t]*)(\S[^=\^\n]+)#%equ(.*)',
                        r"\1\2 \n\1r_mathcomment('''```\2``` \3''' % vars_formated())",
                        script  )
                        
    #--One line comment syntax (indentation acceptable)
    script = re.sub(    r'#![ ]*(.+)',
                        r"r_comment('''\1''' % vars_formated())",
                        script  )
    #--Multi line comment syntax (indentation not acceptable)
    script = re.sub(    r"#!(.{1})'''(.+?)'''",
                        r"r_comment('''\2''' % vars_formated())", 
                        script, flags=re.DOTALL )
    #--One line python code showing syntax (indentation not acceptable)
    script = re.sub(    r"(.+)#%code",
                        r"\1\nr_comment('''```\1```''' )",
                        script  )
    #--Multi line python code showing syntax (indentation not acceptable)
    script = re.sub(    r"#%code(.+?)#%", 
                        r"\1r_comment('''```\1```''' )",
                        script, flags=re.DOTALL )
    #--Image showing syntax (indentation acceptable)
    script = re.sub(    r'#%img (.+)',
                        r"r_img('\1')", 
                        script  )
    #--Matplotlib plt figure syntax (indentation acceptable)
    script = re.sub(    r'([ \t]*)(\w+)(.+)#%plt',
                        r"\1\2\3 \n\1r_plt(\2)",
                        script)
    #--Pillow Image syntax (indentation acceptable)
    script = re.sub(    r'([ \t]*)(\w+)(.+)#%pil',
                        r"\1\2\3 \n\1r_pil(\2)",
                        script)
    #--One line LaTex syntax comment rendering (indentation acceptable)
    script = re.sub(    r'#%tex[ ]*(.+)',
                        r"r_tex(r'\1' % vars())", 
                        script  )
    #--Rendering LaTex syntax from python string (indentation acceptable)
    script = re.sub(    r'([ \t]*)(\w+)\s*#%stringtex',
                        r"\1\2 \n\1r_tex(\2)",
                        script)
    #--One line code rendering as LaTex syntax (indentation acceptable)
    script = re.sub(    r'([ \t]*)(\w[^\n]+)#%tex',
                        r"\1\2 \n\1r_codetex(r'\2' % vars_formated())",
                        script  )
    #--Rendering SVG syntax from python string (indentation acceptable)
    script = re.sub(    r'([ \t]*)(\w+)(.+)#%svg',
                        r"\1\2\3 \n\1r_svg(\2)",
                        script)
    #--Adjustable wariable with one line comment syntax (indentation not tested yet)
    script = re.sub(r'#(<{2,})', r"#\1_idx_", script)
    no = 1  
    while re.search(r"#<{2,}_idx_", script):
        script = script.replace(r'<_idx_', r"<_id%s_" % no, 1)
        no += 1
    script = re.sub(    r'([ \t]*)(\w+)(.+)#<<_(id\d+)_(.+)', 
                        r"\1\2\3 \n\1r_adj('''```\2 = %(\2)s```''' % vars_formated(),'\4','\5' % vars_formated(), 1, '''\2\3''')",
                        script  )
    script = re.sub(    r'([ \t]*)(\w+)(.+)#<<<_(id\d+)_(.+)', 
                        r"\1\2\3 \n\1r_adj('%(\2)s' % vars_formated(),'\4','\5' % vars_formated(), 1, '''\2\3''')",
                        script  )
    script = re.sub(    r'([ \t]*)(\w+)(.+)#<<<<_(id\d+)_(.+)', 
                        r"\1\2\3 \n\1r_adj('%(\2)s' % vars_formated(),'\4','\5' % vars_formated(), 2,  '''\2\3''')",
                        script  )
                        
    #--calling variable with val_name and var_name
    script = re.sub(r'val_(\w+)', r''' ```%(\1)s``` ''', script)
    script = re.sub(r'var_(\w+)', r''' ```\1 = %(\1)s``` ''', script)
    return script