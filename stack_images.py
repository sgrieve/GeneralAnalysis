# -*- coding: utf-8 -*-
"""
Created on Thu Aug 06 20:39:57 2015

@author: Stuart
"""

import Image
import os

def three_stack(path):

    files = os.listdir(path)
    
    a = Image.open(path+files[0])
    b = Image.open(path+files[1])
    c = Image.open(path+files[2])
        
    d = Image.new('RGB', (4000, 9000))
    
    d.paste(a,(0,0))
    d.paste(b,(0,3000))
    d.paste(c,(0,6000))
    
    d.save(path+'three_stack.png',quality=100)
        
def two_stack(path):

    files = os.listdir(path)
    
    a = Image.open(path+files[0])
    b = Image.open(path+files[1])
        
    c = Image.new('RGB', (4000, 6000))
    
    c.paste(a,(0,0))
    c.paste(b,(0,3000))
    
    c.save(path+'two_stack.png',quality=100)
    
def four_panel(path):

    files = os.listdir(path)
    
    a = Image.open(path+files[0])
    b = Image.open(path+files[1])
    c = Image.open(path+files[0])
    d = Image.open(path+files[1])
        
    e = Image.new('RGB', (8000, 6000))
    
    e.paste(a,(0,0))
    e.paste(b,(4000,0))
    e.paste(c,(0,3000))
    e.paste(d,(4000,3000))
    
    e.save(path+'four_panel.png',quality=100)

path = 'C:/Users/Stuart/Dropbox/e_r_paper/figs/avg_method_comparison/'    

two_stack(path)    
#three_stack(path)
#four_panel(path)
