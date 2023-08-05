from PIL import Image, ImageDraw

imagefilepath = '/home/....../someimage.jpg'  #<<<< Image path -

im = None

try:
    im = Image.open(imagefilepath)
except:
    None
    #! File not find

if im:
    #!---
    doshow = False #<<<< Show loaded image
    if doshow:
        #! *Loaded image viev*
        im #%pil
    #! ---
    doresize = True #<<<< Resizing
    if doresize:
        a = 400 #<<<< >>width
        b = 400 #<<<< >>high
        im = im.resize((a,b))
    #! ---
    dorotate = False #<<<< Rotating
    if dorotate :       
        angle = 0 #<<<< >>rotate angle [deg] -
        im = im.rotate(angle)
    #! ---
    doblack = False #<<<< Black white
    if doblack :       
        im = im.convert(mode = 'L')
    #!---
    #! Finaly image looking
    im #%pil
    #!---
    savefilepath = '/home/lukaszlab/Pulpit/alamakota.jpg' #<<<< Save as -
    dosave = False #<<<< Save
    if dosave :
        im.save(savefilepath)
        #! Saved to val_savefilepath!!
        pass
    

