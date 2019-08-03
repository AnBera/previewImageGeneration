import webscreenshot
import pymongo

#db.Bookmarks.update({}, {$unset:{is_image_generated:1}}, {multi:true})

client = pymongo.MongoClient()
db = client['Bookmarkbuddy']
collection = db['Bookmarks']
while 1:
	print("Polling\n")
	for x in collection.find({ "is_image_generated": {"$exists": False} }):#.limit(10):
		try:
			img_path = "D:\\home\\site\\wwwroot\\linkpreview\\images\\"
			webscreenshot.take_webscreenshot(x["url"], img_path+x["imageName"] )
			x["is_image_generated"] = True
			collection.save(x)
		except:
			x["is_error_in_generation"] = True
			collection.save(x)
			print("Oops! exception occured.")
			print()
#webscreenshot.take_webscreenshot("https://twitter.com/ShashiTharoor?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor", "twitterShashiTharoor.png")
#webscreenshot.take_webscreenshot("https://timesofindia.indiatimes.com/india/mamata-banerjees-appeasement-policy-killed-bengals-peace-outgoing-governor-kn-tripathi/articleshow/70415430.cms", "timesMamata.png")
#webscreenshot.take_webscreenshot("https://www.ndtv.com/india-news/kargil-diwas-wont-come-under-any-pressure-when-it-comes-to-national-security-pm-modi-2076371", "ndtvModi.png")
#webscreenshot.take_webscreenshot("https://github.com/ayanb07", "gitHubAyan.png")
#db.Bookmarks.insert({"url":"https://github.com/ayanb07", "imageName":"gitHubAyan.png", "hitCount":0})
#db.Bookmarks.insert({"url":"https://twitter.com/ShashiTharoor?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor", "imageName":"twitterShashiTharoor.png", "hitCount":0})
#db.Bookmarks.insert({"url":"https://timesofindia.indiatimes.com/india/mamata-banerjees-appeasement-policy-killed-bengals-peace-outgoing-governor-kn-tripathi/articleshow/70415430.cms", "imageName":"timesMamata.png", "hitCount":0})
#db.Bookmarks.insert({"url":"https://www.ndtv.com/india-news/kargil-diwas-wont-come-under-any-pressure-when-it-comes-to-national-security-pm-modi-2076371", "imageName":"ndtvModi.png", "hitCount":0})
