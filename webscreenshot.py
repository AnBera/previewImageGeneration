from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import numpy as np
import scipy.stats
import urllib.request

options = Options()
options.headless=True
CHROME_DRIVER_PATH = r'C:\Users\ayanb\Documents\BookmarkBuddy\chromedriver.exe'
driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, chrome_options=options)

def score( array ):
	return scipy.stats.rankdata(array)

def take_webscreenshot(url, imagename):
	driver.get(url)
	driver.maximize_window()
	images = driver.find_elements_by_tag_name("img")
	view_port = driver.get_window_size()
	h_view_port = view_port['height']
	w_view_port = view_port['width']
	view_port_area = h_view_port*w_view_port
	image_size = []
	aspect_ratio1 = []#16/9 or 4/3
	aspect_ratio2 = []#16/9 or 4/3
	position = []
	area_ratio = []
	weight = []
	for image in images:
		h = image.rect['height']+0.001
		w = image.rect['width']+0.001
		x = image.rect['x']+0.001
		y = image.rect['y']+0.001
		weight.append(0.0)
		image_size.append(h*w)
		aspect_ratio1.append( 1/(0.001+np.abs(16.0/9.0 - float(np.maximum(h,w))/float(np.minimum(h,w)))) )#16/9 or 4/3
		aspect_ratio2.append( 1/(0.001+np.abs(4.0/3.0 - float(np.maximum(h,w))/float(np.minimum(h,w)))) )#16/9 or 4/3
		position.append(-y)
		area_ratio.append( float(h*w)/float(view_port_area) )
	weight = np.add( weight, score(image_size) )
	aspect_ratio = np.maximum(aspect_ratio1, aspect_ratio2)
	weight = np.add( weight, score(aspect_ratio) )
	weight = np.add( weight, score(position) )
	weight = np.add( weight, score(area_ratio) )
	print(weight)
	if len(weight) == 0 :
		driver.save_screenshot(imagename)
	else:
		max_index = np.argmax(weight)
		print("Before Test : "+ str(max_index) +"\n")
		src = images[max_index].get_attribute('src')
		print("Test\n")
		print(src)
		urllib.request.urlretrieve(src, imagename)