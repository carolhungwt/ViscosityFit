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
from helper import retriveCircle, imageCenter, getCentroid, getMoment

debug = 0

def getA(img):
  shape = np.shape(img)
  Asum = 0
  for i in range(shape[0]):
    for j in range(shape[1]):
      intensity = img[i][j]
      tempval = intensity
      Asum = Asum+tempval
  M = getMoment(img,iscircle=0,canny=1)
  if debug:  print('m00: '+str(int(M['m00']))+' A: '+str(int(Asum)))
  return Asum

def getxbar(img):
  shape = np.shape(img)
  xbar = 0
  for j in range(shape[0]):
    for i in range(shape[1]):
      intensity = img[j][i]
      #if intensity!=0:  print(' '.join([str(i),str(j),str(intensity)]))
      tempval = i*intensity
      xbar = xbar+tempval
  xbar = xbar/getA(img)
  M = getMoment(img,iscircle=0,canny=1)
  if debug:  print('mu10: '+str(int(M['m10']/M['m00']))+' xbar: '+str(int(xbar)))
  return xbar

def getybar(img):
  shape = np.shape(img)
  ybar = 0
  for j in range(shape[0]):
    for i in range(shape[1]):
      intensity = img[j][i]
      tempval = j*intensity
      ybar = ybar+tempval
  M = getMoment(img)
  ybar = ybar/getA(img)
  if debug:  print('mu01: '+str(int(M['m01']/M['m00']))+' ybar: '+str(int(ybar)))
  return ybar

def geta(img, xbar):
  shape = np.shape(img)
  Asum = 0
  for j in range(shape[0]):
    for i in range(shape[1]):
      intensity = img[j][i]
      if intensity!=0 and intensity!=255:  print(i,j,intensity)
      tempval = (i-xbar)*(i-xbar)*intensity
      Asum = Asum+tempval
  M = getMoment(img)#,iscircle=0,canny=1)
  a = M['mu20']
  #a = np.around(M['mu20'])
  if debug:  print('mu20: '+str(a)+' a: '+str(int(Asum))+' ratio: '+str(int(Asum/a)))
  return Asum

def getb(img, xbar, ybar):
  shape = np.shape(img)
  Bsum = 0
  for j in range(shape[0]):
    for i in range(shape[1]):
      intensity = img[j][i]
      if intensity!=0 and intensity!=255:  print(i,j,intensity)
      tempval = 2*(i-xbar)*(j-ybar)*intensity
      Bsum = Bsum+tempval
  M = getMoment(img)#,iscircle=0,canny=1)
  b = 2*M['mu11']
  #b = np.around(M['mu11'])
  if debug:  print('mu11: '+str(b)+' b: '+str(int(Bsum))+' ratio: '+str(int(Bsum/b)))
  return Bsum

def getc(img, ybar):
  shape = np.shape(img)
  Csum = 0
  for j in range(shape[0]):
    for i in range(shape[1]):
      intensity = img[j][i]
      if intensity!=0 and intensity!=255:  print(i,j,intensity)
      tempval = (j-ybar)*(j-ybar)*intensity
      Csum = Csum+tempval
  M = getMoment(img)#,iscircle=0,canny=1)
  c = M['mu02']
  #c = np.around(M['mu02'])
  if debug:  print('mu02: '+str(c)+' c: '+str(int(Csum))+' ratio: '+str(int(Csum/c)))
  return Csum

def secondMoment(img,**kwargs):
  shape = np.shape(img)
  #cv2.imshow('img',img)
  #cv2.waitKey(0)
  #img = cv2.Canny(img,50,200)
  #img = cv2.GaussianBlur(img,(3,3),0,0)
  #if debug:  
  #  print(circle)
  #  print(getCentroid(img))
  #xbar, ybar = circle[0], circle[1]
  #imagecenter = getCentroid(img)
  #imagecenter = circle[:2]
  #xbar, ybar = imagecenter[0],imagecenter[1]
  A , xbar, ybar = getA(img), getxbar(img), getybar(img)
  if debug:  print(A , xbar, ybar)
  a, b, c = geta(img, xbar), getb(img, xbar, ybar), getc(img, ybar)
  theta = 0.5*np.arctan(b/(a-c))
  theta1 = 0.5*np.arcsin(b/np.sqrt(b*b+(a-c)*(a-c)))
  theta2 = 0.5*np.arccos((a-c)/np.sqrt(b*b+(a-c)*(a-c)))
  theta = [theta,theta1, theta2]
  return theta
