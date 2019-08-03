from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import numpy as np
import scipy.stats
import urllib.request

options = Options()
options.headless=True
CHROME_DRIVER_PATH = r'D:\previewImageGeneration\chromedriver.exe'
driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, chrome_options=options)

def score( array ):
	return scipy.stats.rankdata(array)

def my_debug( images, feature ):
	#print( map(return_image_sting, images) )
	print( feature )
	print( score(feature) )

def take_webscreenshot(url, imagename):
	driver.get(url)
	driver.maximize_window()
	images = driver.find_elements_by_tag_name("img")
	view_port = driver.get_window_size()
	print("View port "+str(view_port))
	h_view_port = view_port['height']
	w_view_port = view_port['width']
	view_port_area = h_view_port*w_view_port
	print("View port area "+str(view_port_area))
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
	# aspect_ratio1 [ 1/0.1 1/0.001]
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
		print("Current Image URL\n")
		print(src)
		print(image.rect)
		print(image_size[i])
		print(weight1[i])
		print(aspect_ratio1[i])
		print(aspect_ratio2[i])
		print(weight2[i])
		print(position[i])
		print(weight3[i])
		print(height_ratio[i])
		print(width_ratio[i])
		print(weight4[i])
		i=i+1
	#Debug End
	max_index = np.argmax(weight)
	print("Dominant Image height_ration : "+str(height_ratio[max_index]))
	print("Dominant Image width_ration : "+str(width_ratio[max_index]))
	print("Dominant Image rect "+ str(images[max_index].rect))
	src = images[max_index].get_attribute('src')
	print("Dominant Image URL\n")
	print(src)
	if len(weight) == 0 or height_ratio[max_index] < 0. or width_ratio[max_index]< 0.075:
		driver.save_screenshot(imagename)
	else:
		print("Before Test : "+ str(max_index) +"\n")
		src = images[max_index].get_attribute('src')
		print("Test\n")
		print(src)
		opener=urllib.request.build_opener()
		opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
		urllib.request.install_opener(opener)
		urllib.request.urlretrieve(src, imagename)