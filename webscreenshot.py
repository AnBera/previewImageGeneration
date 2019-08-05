from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from reportlab.graphics import renderPM
import svglib.svglib
import reportlab.graphics
import numpy as np
import scipy.stats
import urllib.request
import logapi
import os

options = Options()
options.headless=True
options.add_argument('--disable-logging')
CHROME_DRIVER_PATH = r'D:\previewImageGeneration\chromedriver.exe'
driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, chrome_options=options, service_log_path='NUL')

logger = logapi.get_logger_instance()

def score( array ):
	return scipy.stats.rankdata(array)

def my_debug( images, feature ):
	#print( map(return_image_sting, images) )
	logger.debug( feature )
	logger.debug( score(feature) )

def take_webscreenshot(url, imagename):
	driver.get(url)
	driver.maximize_window()
	images = driver.find_elements_by_tag_name("img")
	#images = images + driver.find_element_by_tag_name("svg")
	view_port = driver.get_window_size()
	logger.debug("View port: "+str(view_port))
	h_view_port = view_port['height']
	w_view_port = view_port['width']
	view_port_area = h_view_port*w_view_port
	logger.debug("View port area: "+str(view_port_area))
	image_size = []
	aspect_ratio1 = []#16/9 or 4/3
	aspect_ratio2 = []#16/9 or 4/3
	position = []
	height_ratio = []
	width_ratio = []
	weight = []
	#aspect_ratio weighting factor all feature weighting factor [image_size=0.15, aspect_ration=0.05, position= 0.45, area_ration=0.35]
	weight_factor = [0.15, 0.05, 0.45, 0.35]
	#area_ration convert product to sum
	for image in images:
		h = image.rect['height']+0.001
		w = image.rect['width']+0.001
		x = image.rect['x']+0.001
		y = image.rect['y']+0.001
		weight.append(0.0)
		image_size.append(h*w)
		aspect_ratio1.append( 1/(0.001+np.abs(16.0/9.0 - float(np.maximum(h,w))/float(np.minimum(h,w)))) )#16/9 or 4/3
		aspect_ratio2.append( 1/(0.001+np.abs(4.0/3.0 - float(np.maximum(h,w))/float(np.minimum(h,w)))) )#16/9 or 4/3
		if y < 0:
			y = y % h_view_port # this is to handle images above view port : bring them from below
		position.append(-y)#append -y to make image coming first more dominant
		height_ratio.append( float(h)/float(h_view_port) )
		width_ratio.append( float(w)/float(w_view_port) )
	# image_size [ 100, 10000, 150000 ]
	# aspect_ratio1 [ 1/0.1 1/0.001 ]
	weight1 = weight_factor[0]*score(image_size)
	#my_debug( images, image_size )
	aspect_ratio = np.maximum(aspect_ratio1, aspect_ratio2)
	weight2 = weight_factor[1]*score(aspect_ratio)
	weight3 = weight_factor[2]*score(position)
	weight4 = weight_factor[3]*np.add( score(height_ratio), score(width_ratio) )
	#print(weight)
	weight = np.add(weight, weight1)
	weight = np.add(weight, weight2)
	weight = np.add(weight, weight3)
	weight = np.add(weight, weight4)
	#weight = np.add( weight1, weight2, weight3, weight4 )
	#Debug start
	i=0
	for image in images:
		src = image.get_attribute('src')
		logger.debug("\n")
		logger.debug("Current Image URL: ")
		logger.debug(src)
		logger.debug("Image Rect: "+str(image.rect))
		logger.debug("Image size: "+str(image_size[i]))
		logger.debug("Weight of image size: "+str(weight1[i]))
		logger.debug("Aspect Ratio 16/9: "+str(aspect_ratio1[i]))
		logger.debug("Aspect Ratio 4/3: "+str(aspect_ratio2[i]))
		logger.debug("Weight of Aspect Ratio: "+str(weight2[i]))
		logger.debug("Position of Image: "+str(position[i]))
		logger.debug("Weight of Position of Image: "+str(weight3[i]))
		logger.debug("Height Ratio of image w.r.t view port: "+str(height_ratio[i]))
		logger.debug("Width Ratio of image w.r.t view port: "+str(width_ratio[i]))
		logger.debug("Weight of width and height ratio: "+str(weight4[i]))
		i=i+1
	#Debug End
	try:
		max_index = np.argmax(weight)
		logger.debug("Dominant Image height_ration : "+str(height_ratio[max_index]))
		logger.debug("Dominant Image width_ration : "+str(width_ratio[max_index]))
		logger.debug("Dominant Image rect "+ str(images[max_index].rect))
		src = images[max_index].get_attribute('src')
		logger.debug("Dominant Image URL\n")
		logger.debug(src)
		if len(weight) == 0 or height_ratio[max_index] < 0.1 or width_ratio[max_index]< 0.075:
			driver.save_screenshot(imagename)
		else:
			logger.debug("Before Test : "+ str(max_index) +"\n")
			src = images[max_index].get_attribute('src')
			logger.debug("After Test\n")
			logger.debug(src)
			opener=urllib.request.build_opener()
			opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
			urllib.request.install_opener(opener)
			if src[-4:] == ".svg":#compares last 4 chars of string
				img = os.path.splitext(imagename)[0]+'.svg'
				urllib.request.urlretrieve(src, img)
				drawing = svglib.svglib.svg2rlg(img)
				renderPM.drawToFile(drawing, imagename, fmt="PNG")
			else:
				urllib.request.urlretrieve(src, imagename)
	except:
		driver.save_screenshot(imagename)