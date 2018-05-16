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
from helper import retriveCircle, imageCenter

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

def secondMoment(img,**kwargs):
  shape = np.shape(img)
  img = cv2.GaussianBlur(img,(3,3),0,0)
  circle = retriveCircle(img,method='gaussian')
  xbar, ybar = circle[0], circle[1]
  #imagecenter = imageCenter(img)
  #xbar, ybar = imagecenter[0],imagecenter[1]
  a, b, c = geta(img, xbar), getb(img, xbar, ybar), getc(img, ybar)
  #theta = 0.5*np.arctan(b/(a-c))
  theta1 = np.arcsin(b/np.sqrt(b*b+(a-c)*(a-c)))
  theta2 = np.arccos((a-c)/np.sqrt(b*b+(a-c)*(a-c)))
  theta = [theta1, theta2]
  return theta
