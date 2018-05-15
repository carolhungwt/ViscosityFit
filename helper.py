#helper.py
import cv2, numpy, os, subprocess 

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


def crop(image, circle):
  cx = circle[0]
  cy = circle[1]
  radius = circle[2]
  xup, xlow = cx+radius, cx-radius
  yup, ylow = cy+radius, cy-radius
  cropped = image[ylow:yup,xlow:xup,:]
  return cropped