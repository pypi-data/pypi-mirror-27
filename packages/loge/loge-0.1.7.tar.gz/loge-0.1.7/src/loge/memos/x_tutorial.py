#! #*Loge tutorial*

#%img x_start.png

#!
'''
Please look at Loge report window and your tutorial *.py file editor that has just run.
Please try to change the scrip in editor and use save<Ctrl+s> to see how report has changed.
But first check does the watch script option in toolbar is active.
'''

#! ------------------------------------------------------------

#! Let's write some python script to do some calculations.

a = 12
b = 25
c = a + b

print(a)


#!
'''
You can run this script as normal *.py script - run it by <F5> in script editor.
You have seen the `a` value in shell output. But you can see it in your Loge report ...
'''

a #! - here it is

#! Let's change a value 

a = 30 #! - here is changed value


#! ------------------------------------------------------------

#!
'''
You can call variable values in this comments.
So, we have %(a)s , %(b)s and %(c)s.

And the other way is val_a and var_a
'''

#! ------------------------------------------------------------

#!
'''
You can still run this script as
normal *.py script - run it by <F5> in script editor.
As you can guess python engine does't see the Loge syntax.
'''

#! ------------------------------------------------------------

#!
'''
Loge comments use Markdown.

#Title
##Title
###Title

*some text*

**some text**

* Title
* Title2

More about Markdown you can see here
www.daringfireball.net/projects/markdown/

Here is Markdown tutorial
www.markdowntutorial.com/
'''

#! ------------------------------------------------------------

#! You can see python code from your script in Loge report

#%code
r = 120
import math
math.pi
area = math.pi * r ** 2
#%

#! for one line code

area = math.pi * r ** 2 #%code


area #!- here is what we get

#! ------------------------------------------------------------

#! Go to Script>Float precission in menu to change float precission.

#! ------------------------------------------------------------

#!
'''
Lets show image in your report,
the image file must be storef in the same directory where you script is.
'''

#%img x_python.png

#! ... here our Python is.

#! ------------------------------------------------------------
#!
'''
The Python Imaging Library adds image processing capabilities to your Python interpreter.
You can display image from PIL.Image instance. Here is ismply example, it will display resized 
and rotated image.
'''
import os
from PIL import Image
imagefilepath = '/home/.../someimage.jpg' #<<<< Click to select image path (jpg,png..)  -
if os.path.isfile(imagefilepath):
    im = Image.open(imagefilepath) 
    #! Resizeing
    im = im.resize((200,200)) #%pil
    #! Rotating
    angle = 40 #<<<< Rotate angle - 
    im2 = im.rotate(angle) #%pil

#! Here you can find more about PILLOW www.pillow.readthedocs.io/en/3.4.x/index.html

#! ------------------------------------------------------------

#! What about plotting?? You can use Matplotlib pyplot - here is some example

import matplotlib.pyplot as plt
import numpy as np
t = np.arange(-1.0, 2.0, 0.01)
s1 = np.cos(9*np.pi*t) + 3 * t ** 2
plt.plot(t, s1)
plt #%plt
plt.clf()

#! ------------------------------------------------------------

#! If you need to publish some mathematical formula LaTex syntax can be used

#! You can write some LaTex as comment
#%tex s(t) = \mathcal{A}\mathrm{sin}(2 \omega t)

#! or if the LaTex fomula is in you python code
pi = 3.14
r = 40
Area = pi * r ** 2 #%tex

#! or if the LaTex fomula is defined as python string
LaTexString = '\lim_{x \to \infty} \exp(-x) = 0'
LaTexString #%stringtex

#! ------------------------------------------------------------

#!
'''
You can change python variables in report, so finally you don't need to edit
script source to change input data.
'''

a = 120 #! - this is not interactive variable in your report
b = 66 #<< - this is interactive variable in your report - click to change it
#! Those values are var_a and var_b.

#! Other display effects are possible
b = 66 #<< your comment
b = 66 #<<< your comment
b = 66 #<<<< your comment

#! If your variable is equal some list element, you can select list element interactively:
somelist = [1, 2, 3, 4]
variable = somelist[2] #<< - select variable value

#! or with othet display effects
variable = somelist[2] #<< - select variable value
variable = somelist[1] #<<< - select variable value
variable = somelist[1] #<<<< select variable value

#! ####There are some special cases available

#! If you variable value is True or False then interactive CheckBox will be displayed on report when  or used. When you click CheckBox the value will change to opposite bool value.
boolvarialbe = True #<<< - click me
#! We have val_boolvarialbe
boolvarialbe = True #<<<< Click me -
#! We have val_boolvarialbe
boolvarialbe = True #<< - click me
#! We have val_boolvarialbe

#! If your variable name has 'filepath' or 'dirpath' in name then file or directory browse dialog will be open after clicked.

image_filepath = '/home/image.ipg' #<<< - click me to get new file path
#! Your file path is val_image_filepath

search_dirpath = '/home' #<<<< Click me to get new dir path -
#! Your file path is val_search_dirpath

#! *Examples of use*

#! ####*Example 1*
car_list = ['volvo', 'toyota', 'saab', 'fiat']
your_car = car_list[0] #<<<< Select your car -
carcolor = 'black' 

getcolor = False #<<<Browse val_your_car color if not val_carcolor
if getcolor:
    car_colors = [ carcolor, 'pink', 'red', 'magenta']
    carcolor = car_colors[0] #<<<< >>Select your color -
#! Your car is val_carcolor  val_your_car .

#! ####*Example 2*
material_list = ['steel', 'concrete', 'plastic', 'wood']
material = material_list[0] #<<<< Material is - 
#! The %(material)s will be used to make something.

#! ####*Example 3*
temperature_range = list(range(10,30,1))
docontrol = False #<<< Temperature control state
if docontrol:
    room_temperature = temperature_range[17] #<<<< Select temperature - 
    #! Temperature %(room_temperature)s Celsius degree selected
else :
    pass
    
#! ------------------------------------------------------------

#! What about drawing in report ?? You can create drawing using SVG syntax.

#! Python string with SVG syntax can be rendered.

svgsyntax='''
<svg height="55" width="55">
    <circle cx="30" cy="30" r="20"
    stroke="black" stroke-width="1" fill="tan" /> 
</svg>
'''
svgsyntax #%svg

#! so this is the way to get parametric drawing

r = 50 #<< - circle radius value
xs = 120 #<< - center x
ys = 70 #<< - center y
svgsyntax='''
<svg height="150" width="200">
    <circle cx="{1}" cy="{2}"
    r="{0}" stroke="black" stroke-width="1" fill="tan" />
    <text x="{1}" y="{2}" fill="black"
    font-size="15">circle {0} radius </text>  
</svg>
'''.format(r, xs, ys)
#! for this parameters we have
svgsyntax #%svg

#!To make parametrise easer you can use `svgwrite` package

import svgwrite
a = 60 #<< - rec a dimension
b = 100 #<< - rec b dimension
svg_document = svgwrite.Drawing(size = (200, 100))
svg_document.add(svg_document.rect(insert = (0, 0), size = (a, b),
                                   stroke_width = "1",stroke = "black",fill = "tan"))
svg_document.add(svg_document.text("Rectangle size" + str(a)+ 'x' +str(b) ,
                                   insert = (a/2-20, b/2)))
svg_document #%svg 

#! ------------------------------------------------------------

#! Mathematical expressions and equations
#! You can add to Loge report expressions and equations with optional comment 
a = 1
b = 3
c = 3*a + 4*b #%requ - your comment
c = 3*a + 4*b #%requ
c = 3*a + 4*b #%equ - your comment
c = 3*a + 4*b #%equ
3*a + 4*b #%requ - your comment
3*a + 4*b #%requ
3*a + 4*b #%equ - your comment
3*a + 4*b #%equ

#! Python code is formated to look more natural

import math
math.pi #%equ
math.sin(1) #%equ
2**2 #%equ

#! When you are working with SI units using Unum package

from unum import units as u
5 * u.m + 10 * u.mm #%requ
(5 * u.m + 10 * u.mm).asUnit(u.km) #%equ

#! ------------------------------------------------------------

#! ##Go to Info>Syntax help to get know abaut all available  Loge syntax.
