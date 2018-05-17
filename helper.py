#helper.py
import cv2, numpy, os, subprocess 

debug =0

def pwd():
  cwd = os.getcwd()
  return cwd

#https://stackoverflow.com/questions/273192/how-can-i-create-a-directory-if-it-does-not-exist
def makedir(basedir, foldername):
  newdir = os.path.join(basedir,foldername)
  if not os.path.exists(newdir):
    os.makedirs(newdir)
  return newdir

def readdir(dirpath):
	assert type(dirpath) is str
	abspath = os.path.abspath(dirpath)
	ls_output = subprocess.getoutput(['ls '+dirpath])
	lines = ls_output.split('\n')
	pics = []
	withimages = False
	for line in lines:
		if '.tif' in line:
			withimages = True
			imagepath = os.path.join(abspath,line)
			if not os.path.exists(imagepath):  raise IOError(imagepath+' does not exist. Check readdir function')
			pics.append(imagepath)
	if not withimages:
		raise AssertionError("No images found in the given directory")
	return pics


def readimage(picdir):
	assert type(picdir) is str
	try: 
		rim = cv2.imread(picdir)
		return rim
	except:
		raise IOError(picdir+' does not exist.')

def flattened(cropped):
  shape = numpy.shape(cropped)
  shape = (shape[0],shape[1])
  flat = numpy.ndarray(shape,cropped.dtype)
  for i in range(shape[0]):
    for j in range(shape[1]):
      temp = cropped[i][j][0]
      flat[i][j] = temp
  return flat

#https://stackoverflow.com/questions/17870612/printing-a-two-dimensional-array-in-python
def disp(img):
  A = img
  print('\n'.join([''.join(['{:3}'.format(item) for item in row]) 
      for row in A]))

def saveimage(savepath, img):
  cv2.imwrite(savepath, img)


def crop(image, circle, **kwargs):
  rim = 5
  for k,v in kwargs.items():
    if k == 'rim':  rim = int(v)
  cx = circle[0]
  cy = circle[1]
  radius = circle[2]+rim  #default is 5
  xup, xlow = cx+radius, cx-radius
  yup, ylow = cy+radius, cy-radius
  cropped = image[ylow:yup,xlow:xup,:]
  return cropped

def selectBiggestCircle(circles):
  selcircle,R = 0.,0
  for i,circle in enumerate(circles):
    _,_,curR = circle[i]
    if curR > R:  
      selcircle = circle[i]
  debug=0
  if debug:  print(selcircle)
  selcircle[2]=selcircle[2]
  return selcircle


def retriveCircle(refimg,**kwargs):
  circle = []
  for (k,v) in kwargs.items():
    k = k.lower()
    if k == 'method':
      if v == 'hough':
        circle = getCirclewithHough(refimg,method='gaussian')
      elif v == 'contour':
        circle = getCirclewithContour(refimg)
      else:
        raise Exception('method entered for circle retrival: '+str(v))
  if circle == []:
    raise Exception('Cannot retrive circle from the image. Tune parameters and try again.')
  return circle


def getCirclewithContour(refimg):
  tempimg = refimg
  contour = getContour(refimg)
  center, radius = cv2.minEnclosingCircle(contour)
  circle = [center[0],center[1],radius]
  circle = numpy.uint16(numpy.around(circle))
  return circle


def getCirclewithHough(refimg,**kwargs):
  #default mehtod is cv2.Canny edge detection, no noise reduction
  tempimg = refimg
  for (k,v) in kwargs.items():
    if k == 'method':
      if v == 'gaussian':
        tempimg = cv2.GaussianBlur(refimg,(3,3),0,0)
  preprocessed = cv2.Canny(tempimg,100,150)
  #Using HoughCircle
  circles = cv2.HoughCircles(preprocessed,cv2.HOUGH_GRADIENT,1,50,param1=50,param2=20,minRadius=10,maxRadius=80)
  #Using contour 
  #circles = getContour(canny)
  circles = numpy.uint16(numpy.around(circles))
  #no debugging 
  if debug: 
    cv2.imshow('preprocessed',preprocessed)
    cv2.waitKey(0)
    output = refimg.copy()
    for (x,y,r) in circles[0]:
      cv2.circle(output, (x, y), r, (0, 220, 0), 2)
      cv2.rectangle(output, (x - 2, y - 2), (x + 2, y + 2), (0, 128, 255), -1)
    cv2.imshow("output", numpy.hstack([refimg, output]))
    cv2.waitKey(0)
  circle = selectBiggestCircle(circles)
  circle = numpy.uint16(numpy.around(circle))
  return circle

def imageCenter(img):
  tempimg = img
  shape = numpy.shape(img)
  center = [int(shape[0]/2),int(shape[1]/2)]
  return center

def getImageIndex(picpath):
  #10G_static_20Mag_125fps000089.tif
  tags = picpath.split('_')[-1]
  tag = tags.split('.tif')[0]
  index = tag[-2:]
  return index



def getContour(img):
  debug =0
  canny = cv2.Canny(img,100,150)
  _, contours, _= cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  contour_list = []
  for contour in contours:
    approx = cv2.approxPolyDP(contour,0.01*cv2.arcLength(contour,True),True)
    area = cv2.contourArea(contour)
    if debug:
      print(len(approx),area)
    if len(approx) > 8 and (area>20):
      contour_list.append(contour)  
  if not contour_list:  
    debugpath = os.path.join(pwd(),'debug_getContour.png');
    debugoriginalpath = os.path.join(pwd(),'debug_original_getContour.png');
    cv2.imwrite(debugoriginalpath,img)
    cv2.imwrite(debugpath,canny)
    print('******************\n'+debugoriginalpath+' has been created\n' \
      +debugpath+' has been created\n ************************')
    raise Exception('contour_list is empty, change selection criteria and try again')
  largestdisk = contour_list[0]
  if len(contour_list)>1:
    for contour in contour_list:
      if cv2.contourArea(contour)>cv2.contourArea(largestdisk):
        largestdisk = contour 
  return largestdisk

def getCentroid(img):
  contour = getContour(img)
  M = cv2.moments(contour)
  if debug:  print(M)
  try: 
    cx = M['m01']/M['m00']
    cy = M['m02']/M['m00']
  except ZeroDivisionError:
    print('Finding contour failed')
  centroid = [cx,cy]
  return centroid

from math import hypot
def circularMasked(img,circle):
  tempimg = img
  x, y, r = circle
  rows, cols = tempimg.shape
  for i in range(cols):
    for j in range(rows):
        if hypot(i-x, j-y) > r:
          tempimg[j,i] = 0
  return tempimg

