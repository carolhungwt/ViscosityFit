#AngleSecondMoment.py

import cv2, os
import numpy as np
from helper import readimage, readdir, crop, flattened, disp, saveimage, retriveCircle, imageCenter, getImageIndex
from secondMoment import secondMoment
from secondMomentNoIntensity import secondMomentNoIntensity

#testpath = '/Users/carolhungwt/Documents/10G_static_20mag_125fps/'
testpath = '/Users/carolhungwt/Documents/Leheny/NanYangDisk/disk2/3GY-2GX-125fps'
debug = 0
v=0

def getContour(canny):
  _, contours, _= cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  contour_list = []
  for contour in contours:
    approx = cv2.approxPolyDP(contour,0.01*cv2.arcLength(contour,True),True)
    area = cv2.contourArea(contour)
    if (len(approx) > 8 and (area>20)):
      contour_list.append(contour)  
      try:
        largestdisk = contour_list[0]
      except Exception:
        print('No disk found in '+self.picdir)
        return
      if len(contour_list)>1:
        for contour in contour_list:
          if cv2.contourArea(contour)>cv2.contourArea(largestdisk):
            largestdisk = contour 
    return largestdisk


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
    cropped = crop(self.original,self.circle, rim=8)
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
  def translated(self):
    tmpobj = self.bkgzeroed
    circle = retriveCircle(tmpobj,method='gaussian')
    imagecenter = imageCenter(tmpobj)
    shiftx = imagecenter[0]-circle[0]
    shifty = imagecenter[1]-circle[1]
    nrow, ncol = tmpobj.shape[:2]
    translationMat = np.float32([ [1,0,shiftx], [0,1,shifty] ])
    translated = cv2.warpAffine(tmpobj, translationMat, (ncol, nrow))
    if debug:
      cv2.imshow('translated',translated)
      waitKey(0)
    return translated

  @property
  def secondMomentAngle(self,Intensity=0):
    tmpobj = self.bkgzeroed
    if Intensity==0:
      theta = secondMomentNoIntensity(tmpobj)
    else:
      theta = secondMoment(tmpobj)
    return theta


if __name__=='__main__':
  pics = readdir(testpath)
  refcircle = 0 
  pics = pics[:50]
  for i,pic in enumerate(pics):
    index = getImageIndex(pic)
    pic = os.path.join(testpath,pic)
    img = readimage(pic)
    if i==0:  refcircle = retriveCircle(img,method='gaussian')
    disk = diskframe(pic, refcircle)
    disk.zeroThreshold = 150
    savepath = os.path.join(testpath,str(i)+'_processed.png')
    #savepath = pic.split('.tif')[0]+'_processed.png'
    saveimage(savepath, disk.bkgzeroed)
    #disp(flattened(disk.bkgzeroed))
    if i==0:  refAngle = disk.secondMomentAngle[0]
    print(index+' '+str(disk.secondMomentAngle[0]-refAngle))

