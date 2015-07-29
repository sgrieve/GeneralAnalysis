# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 11:56:46 2015

@author: Stuart Grieve
"""

import numpy as np
import matplotlib.pyplot as plt


def distbetween(x1,y1,x2,y2):
    """
    Compute the distance between points (x1,y1) and (x2,y2)
    """

    return np.sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1))

def get_circumcircleradius(x1,y1,x2,y2,x3,y3):
    """
    Given points of a triangle (x1,y1),(x2,y2),(x3,y3) get the radius of the circle that
    intersects these points
    
    http://www.bobbymcr.com/main/math/circumcircle.pdf
    """
    
    #first we need the lengths of the 3 sides, a,b,c
    
    a = distbetween(x1,y1,x2,y2)
    b = distbetween(x1,y1,x3,y3)
    c = distbetween(x3,y3,x2,y2)
    
    s = (a+b+c)/2.
    
    area = np.sqrt(s*(s-a)*(s-b)*(s-c))
    
    radius = (a*b*c)/ (area*4.)
    
    return radius
        
def get_circumcenter(x1,y1,x2,y2,x3,y3):
    """
    Get the center point for a circle that intersects a triangle given by (x1,y1),(x2,y2),(x3,y3)
    Also returns the radius, calculateed as the distance between the radius and one of the 
    corners of the triangle.
    
    https://en.wikipedia.org/wiki/Circumscribed_circle
    """
    D = 2.*(x1*(y2-y3) + x2*(y3-y1) + x3*(y1-y2))
    
    x = ( (x1**2.+y1**2.) * (y2-y3) + (x2**2.+y2**2.) * (y3-y1) + (x3**2.+y3**2.) * (y1-y2) ) / D
    
    y = ( (x1**2.+y1**2.) * (x3-x2) + (x2**2.+y2**2.) * (x1-x3) + (x3**2.+y3**2.) * (x2-x1) ) / D
    
    radius = distbetween(x,y,x2,y2)    
    
    return (x,y),radius
        
#first we make some toy data
x = np.array([0.1,1.2,2.4,3.4,3.8,5.2,6.9,7.88,8.5,9.7,10.2,11.67]) #this would be the linear distance between each (x,y) pair
z = np.array([90.,88.,87.,80.,65.,40.,30.,20.,18.,17.,16.,15.]) #this is the elevation of each (x,y) pair

#make our plot equal area so the circles are circular.
plt.axis('equal')

#plot all of the points of our fake trace
plt.plot(x,z,'k.')
fig = plt.gcf()

#cycle through each set of 3 points and get the radius of curvature, plotting it as
# a circle for visualisation purposes.
for i in range(1,11):
    center,radius = get_circumcenter(x[i-1],z[i-1],x[i],z[i],x[i+1],z[i+1])
    
    #test that the center point is correct within 3 decimal places as we have 2 methods of estimating the radius
    if (round(radius,3) == round(get_circumcircleradius(x[i-1],z[i-1],x[i],z[i],x[i+1],z[i+1]),3)):
        #draw the valid circle        
        circle1=plt.Circle(center,radius,color='r',fill=False)
        fig.gca().add_artist(circle1)
    else:
        print 'Something has gone wrong'
    
plt.show()

  



