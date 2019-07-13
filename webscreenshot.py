from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless=True
CHROME_DRIVER_PATH = r'C:\Users\ayanb\Documents\BookmarkBuddy\chromedriver.exe'
driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, chrome_options=options)

def take_webscreenshot(url, imagename):
	driver.get(url)
	driver.save_screenshot(imagename)