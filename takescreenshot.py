import webscreenshot
import pymongo

client = pymongo.MongoClient()
db = client['Bookmarkbuddy']
collection = db['Bookmarks']
while 1:
	print("Polling\n")
	for x in collection.find({ "image_generated": {"$exists": False} }).limit(2):
		webscreenshot.take_webscreenshot(x["url"], x["imageName"])
		x["image_generated"] = True
		collection.save(x)
#webscreenshot.take_webscreenshot("https://twitter.com/ShashiTharoor?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor", "twitterShashiTharoor.png")
#webscreenshot.take_webscreenshot("https://timesofindia.indiatimes.com/india/mamata-banerjees-appeasement-policy-killed-bengals-peace-outgoing-governor-kn-tripathi/articleshow/70415430.cms", "timesMamata.png")
#webscreenshot.take_webscreenshot("https://www.ndtv.com/india-news/kargil-diwas-wont-come-under-any-pressure-when-it-comes-to-national-security-pm-modi-2076371", "ndtvModi.png")
#webscreenshot.take_webscreenshot("https://github.com/ayanb07", "gitHubAyan.png")
#db.Bookmarks.insert({"url":"https://github.com/ayanb07", "imageName":"gitHubAyan.png", "hitCount":0})
#db.Bookmarks.insert({"url":"https://twitter.com/ShashiTharoor?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor", "imageName":"twitterShashiTharoor.png", "hitCount":0})
#db.Bookmarks.insert({"url":"https://timesofindia.indiatimes.com/india/mamata-banerjees-appeasement-policy-killed-bengals-peace-outgoing-governor-kn-tripathi/articleshow/70415430.cms", "imageName":"timesMamata.png", "hitCount":0})
#db.Bookmarks.insert({"url":"https://www.ndtv.com/india-news/kargil-diwas-wont-come-under-any-pressure-when-it-comes-to-national-security-pm-modi-2076371", "imageName":"ndtvModi.png", "hitCount":0})
