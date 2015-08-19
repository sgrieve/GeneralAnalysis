# -*- coding: utf-8 -*-
"""
Created on Thu Aug 06 20:39:57 2015

@author: Stuart
"""

import Image
import ImageFont
import ImageDraw
import os
import string

#set up fonr, supply the path to the font to be used here along with the size of the text
font = ImageFont.truetype("C:\\Windows\\Fonts\\Arial.ttf",200)
labels = list(string.ascii_uppercase)[:4]  #plot labels

def three_stack(path):

    files = os.listdir(path)
    
    a = Image.open(path+files[0])
    b = Image.open(path+files[1])
    c = Image.open(path+files[2])
        
    d = Image.new('RGB', (4000, 9000))
    
    d.paste(a,(0,0))
    d.paste(b,(0,3000))
    d.paste(c,(0,6000))
    
    
    draw = ImageDraw.Draw(d)   
    
    xPlacements = [0,0,0]
    yPlacements = [0,3000,6000]
    
    for i in range(3):
        draw.text((600+xPlacements[i], 350+yPlacements[i]),labels[i],(0,0,0),font=font)       
    
    
    d.save(path+'three_stack.png',quality=100)
        
def two_stack(path):

    files = os.listdir(path)
    
    a = Image.open(path+files[0])
    b = Image.open(path+files[1])
        
    c = Image.new('RGB', (4000, 6000))
    
    c.paste(a,(0,0))
    c.paste(b,(0,3000))

    draw = ImageDraw.Draw(c)   
    
    xPlacements = [0,0]
    yPlacements = [0,3000]
    
    for i in range(2):
        draw.text((600+xPlacements[i], 350+yPlacements[i]),labels[i],(0,0,0),font=font)   
           

    c.save(path+'two_stack.png',quality=100)
    
def four_panel(path):

    files = os.listdir(path)
    
    a = Image.open(path+files[0])
    b = Image.open(path+files[1])
    c = Image.open(path+files[2])
    d = Image.open(path+files[3])
        
    e = Image.new('RGB', (8000, 6000))
    
    e.paste(a,(0,0))
    e.paste(b,(4000,0))
    e.paste(c,(0,3000))
    e.paste(d,(4000,3000))

    draw = ImageDraw.Draw(e)   
    
    xPlacements = [0,4000,0,4000]
    yPlacements = [0,0,3000,3000]
    
    for i in range(4):
        draw.text((600+xPlacements[i], 350+yPlacements[i]),labels[i],(0,0,0),font=font)   
    
    e.save(path+'four_panel.png',quality=100)

path = 'C:/Users/Stuart/Dropbox/e_r_paper/figs/nc_data/'    

#two_stack(path)    
#three_stack(path)
four_panel(path)
