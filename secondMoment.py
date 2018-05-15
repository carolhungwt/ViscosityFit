#secondMoment.py
#*******************************
#To calculate second moment about the image center
#Following the form:
# E = a*sin^2(theta)-b*sin(theta)*cos(theta)+c*cos(theta)
# where a = iint((x-xbar)^2 b(x,y))dxdy
#       b = iint((x-xbar)(y-ybar) b(x,y))dxdy
#       c = iint((y-ybar)^2 b(x,y))dxdy
# To minimize E wrt theta
# tan(2*theta) = b/(a-c)
#*******************************

import cv2
import numpy as np

def geta(img, xbar):
  shape = np.shape(img)
  Asum = 0
  for i in range(shape[0]):
    for j in range(shape[1]):
      intensity = img[i][j][0]
      tempval = (i-xbar)*(i-xbar)*intensity
      Asum = Asum+tempval
  return Asum

def getb(img, xbar, ybar):
  shape = np.shape(img)
  Bsum = 0
  for i in range(shape[0]):
    for j in range(shape[1]):
      intensity = img[i][j][0]
      tempval = 2*(i-xbar)*(j-ybar)*intensity
      Bsum = Bsum+tempval
  return Bsum

def getc(img, ybar):
  shape = np.shape(img)
  Csum = 0
  for i in range(shape[0]):
    for j in range(shape[1]):
      intensity = img[i][j][0]
      tempval = (j-ybar)*(j-ybar)*intensity
      Csum = Csum+tempval
  return Csum

def secondMoment(img):
  shape = np.shape(img)
  xbar, ybar = int(shape[0]/2), int(shape[1]/2)
  a, b, c = geta(img, xbar), getb(img, xbar, ybar), getc(img, ybar)
  theta = 0.5*np.arctan(b/(a-c))
  return theta
