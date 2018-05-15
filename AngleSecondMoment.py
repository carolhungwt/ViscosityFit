#AngleSecondMoment.py

import cv2, os
import numpy as np
from helper import readimage, readdir, crop, flattened, disp, saveimage
from secondMoment import secondMoment

testpath = '/Users/carolhungwt/Documents/10G_static_20mag_125fps/'
debug = 0


def selectBiggestCircle(circles):
  selcircle,R = 0.,0
  for i,circle in enumerate(circles):
    _,_,curR = circle[i]
    if curR > R:  
      selcircle = circle[i]
  selcircle[2]=selcircle[2]+5
  return selcircle

def retriveCircle(refimg):
  canny = cv2.Canny(refimg,50,200)
  #cv2.imshow('canny',canny)
  #cv2.waitKey(0)param1=30,param2=30
  circles = cv2.HoughCircles(canny,cv2.HOUGH_GRADIENT,1,5,param1=250,param2=20,minRadius=0,maxRadius=80)
  circles = np.uint16(np.around(circles))
  if debug: 
    print(circles[0])
    output = refimg.copy()
    for (x,y,r) in circles[0]:
      cv2.circle(output, (x, y), r, (0, 255, 0), 3)
      cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
    #cv2.startWindowThread()
    #cv2.namedWindow("output")
    cv2.imshow("output", np.hstack([refimg, output]))
    cv2.waitKey(0)
    saveimage('~/output.png',output)
  circle = selectBiggestCircle(circles)
  return circle


class diskframe(object):
  def __init__(self,path,circle,**kwargs):
    self.imgpath = path
    self.circle = circle
  
  @property
  def original(self):
    return readimage(self.imgpath)

  @property 
  def ccx(self):
    return self.circle[0]

  @property 
  def ccy(self):
    return self.circle[1]

  @property 
  def radius(self):
    return self.circle[2]

  @property 
  def cropped(self):
    cropped = crop(self.original,self.circle)
    return cropped

  @property
  def zeroThreshold(self):
    return self._zeroThreshold

  @zeroThreshold.setter
  def zeroThreshold(self,value):
    if not (0<= value <= 255):
      raise ValueError('Threshold value must be between 0 and 255')
    self._zeroThreshold=value

  @property
  def bkgzeroed(self):
    tmpobj = self.cropped
    #inverting cropped image
    tmpobj = cv2.bitwise_not(tmpobj)
    shape = np.shape(self.cropped)
    bkgzeroed = np.ndarray(shape,tmpobj.dtype)
    xsize, ysize, rbg = shape[0], shape[1], shape[2]
    for i in range(xsize):
      for j in range(ysize):
        intensity = tmpobj[i][j][0]
        if intensity<self.zeroThreshold:
          for k in range(rbg):
            bkgzeroed[i][j][k]=0
        else:
          for k in range(rbg):
            bkgzeroed[i][j][k]=intensity
    return bkgzeroed        

  @property
  def secondMomentAngle(self):
    tmpobj = self.bkgzeroed
    theta = secondMoment(tmpobj)
    return theta


if __name__=='__main__':
  pics = readdir(testpath)
  refcircle = 0 
  #pics = pics[:2]
  for i,pic in enumerate(pics):
    pic = os.path.join(testpath,pic)
    if i==0:  
      refimg = readimage(pic)
      refcircle = retriveCircle(refimg)
    disk = diskframe(pic, refcircle)
    disk.zeroThreshold = 150
    savepath = pic.split('.tif')[0]+'_processed.png'
    saveimage(savepath, disk.bkgzeroed)
    #disp(flattened(disk.bkgzeroed))
    print(disk.secondMomentAngle)

