import webscreenshot
import pymongo
# import logapi
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bson import ObjectId
import os
from azure.storage.blob import BlockBlobService

# Create the BlockBlockService that is used to call the Blob service for the storage account.

#db.Bookmarks.update({}, {$set:{is_image_generated:true}}, {multi:true})
#db.Bookmarks.find({}).limit(10).forEach( function(doc){ db.Bookmarks.update({_id:doc._id},{$unset:{is_image_generated:true}}) } )

def poll_and_generate_image():
	#========TODO NEED TO CHECK WHETHER IT CAN BE MOVED TO A SINGLEPLACE =====
	# logger = logapi.get_logger_instance()

	client = pymongo.MongoClient("mongodb://XXXX")
	db = client['bmby']
	collection = db['Bookmarks']
	#========================
	#while 1:
	print("Polling\n")
	bookmark_item = collection.find({ "is_image_generated": {"$exists": False} }).limit(1)
	print(bookmark_item[0]["url"])
	count = 0
	for x in bookmark_item:
		if str(x["url"]).startswith("http") or str(x["url"]).startswith("www"):
			objShardToUpdate = str(x["imageName"])[0]
			objIdToUpdate = x["_id"]
			try:
				##logger.debug("--------------------------------BEGIN--------------------------------------------------")
				#logger.debug("URL: "+str(x["url"]))
				#logger.debug("IMAGE: "+str(x["imageName"]))
				webscreenshot.take_webscreenshot(x["url"], x["imageName"] )
				#logger.debug("--------------------------------END----------------------------------------------------")
				#x["is_image_generated"] = True
				#collection.save(x)
				collection.update_one({"_id":ObjectId(objIdToUpdate), "shardInfo":objShardToUpdate}, {"$set": {"is_image_generated":True}})
			except Exception as e:
				print (e)
				#x["is_error_in_generation"] = str(sys.exc_info())
				#collection.save(x)
				collection.update_one({"_id":ObjectId(objIdToUpdate), "shardInfo":objShardToUpdate}, {"$set": {"is_error_in_generated":True}})
				#logger.debug("Oops! exception occured.: "+str(sys.exc_info()))
				#logger.debug("\n")
def initialize():
	try:
		poll_and_generate_image()
	except Exception as e:
		webscreenshot.driver.quit()
		print(e)
		#=======TODO MOVE IT TO A COMMON PLACE AND MAKE THE DRIVER SINGLETON======
		# options = Options()
		# options.headless=True
		# options.add_argument('--disable-logging')
		# CHROME_DRIVER_PATH = './chromedriver'
		# webscreenshot.driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, chrome_options=options, service_log_path='NULL')
		#=======
		#poll_and_generate_image()
#webscreenshot.take_webscreenshot("https://twitter.com/ShashiTharoor?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor", "twitterShashiTharoor.png")
#webscreenshot.take_webscreenshot("https://timesofindia.indiatimes.com/india/mamata-banerjees-appeasement-policy-killed-bengals-peace-outgoing-governor-kn-tripathi/articleshow/70415430.cms", "timesMamata.png")
#webscreenshot.take_webscreenshot("https://www.ndtv.com/india-news/kargil-diwas-wont-come-under-any-pressure-when-it-comes-to-national-security-pm-modi-2076371", "ndtvModi.png")
#webscreenshot.take_webscreenshot("https://github.com/ayanb07", "gitHubAyan.png")
#db.Bookmarks.insert({"url":"https://github.com/ayanb07", "imageName":"gitHubAyan.png", "hitCount":0})
#db.Bookmarks.insert({"url":"https://twitter.com/ShashiTharoor?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor", "imageName":"twitterShashiTharoor.png", "hitCount":0})
#db.Bookmarks.insert({"url":"https://timesofindia.indiatimes.com/india/mamata-banerjees-appeasement-policy-killed-bengals-peace-outgoing-governor-kn-tripathi/articleshow/70415430.cms", "imageName":"timesMamata.png", "hitCount":0})
#db.Bookmarks.insert({"url":"https://www.ndtv.com/india-news/kargil-diwas-wont-come-under-any-pressure-when-it-comes-to-national-security-pm-modi-2076371", "imageName":"ndtvModi.png", "hitCount":0})
