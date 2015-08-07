# -*- coding: utf-8 -*-
"""
Created on Thu Aug 06 20:39:57 2015

@author: Stuart
"""

import Image
import os


path = 'C:\\Users\\Stuart\\Dropbox\\e_r_paper\\figs\\spatial_averaging_comparison\\'

files = os.listdir(path)

b = Image.open(path+files[0])
a = Image.open(path+files[1])
d = Image.open(path+files[2])


c = Image.new('RGB', (4000, 9000))

c.paste(b,(0,0))
c.paste(a,(0,3000))
c.paste(d,(0,6000))

c.save(path+'stack.png',quality=100)