from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import wget
import json
import time

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors-spki-list')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument('log-level=3')
driver = webdriver.Chrome(chrome_options=options)


#Get YT Videos
driver.get("https://www.youtube.com/results?search_query=how+to+ride+a+*")

#aşağıya 2 upload kadar kaydır

##

all_video_urls = []

#get video card
videocards = driver.find_elements(By.XPATH, "//ytd-video-renderer")
for i in videocards:
	videourl = i.find_element(By.TAG_NAME, "a").get_attribute("href")
	all_video_urls.append(videourl)


#Video Loop Getting Datas
for url in all_video_urls[:5]:

	f = open("database.txt", "a", encoding="utf8")

	dic = {"title":"", "imgname":"", "comments": ""}

	driver.get(url)
	time.sleep(5)

	#header = driver.find_element(By.XPATH, "//div[@id='title']")
	title = driver.find_elements(By.XPATH, "//h1")
	title = title[1].text

	dic["title"] = title

	#scroll

	comments = driver.find_elements(By.XPATH, "//ytd-comment-thread-renderer")
	
	commentappend = ""

	for comment in comments[:10]:
		if "Pinned by" in comment.text:
			pass
		else:
			comment_body = comment.find_element(By.XPATH, ".//div[@id='comment-content']").text.replace("\n","")
			comment_body = comment_body.replace('"','')
			comment_body = comment_body.encode("ascii", "ignore")
			comment_body = comment_body.decode()

			commentappend += comment_body


	dic["comments"] = commentappend

	#Thumbnail
	url = url.split('watch?v=')
	videoID = url[1]
	imgUrl = f"https://img.youtube.com/vi/{videoID}/maxresdefault.jpg"

	driver.get(imgUrl)
	img = driver.find_element(By.TAG_NAME, "img")
	img.screenshot("{}.jpg".format(videoID))

	dic['imgname'] = videoID

	turndic = json.dumps(dic)
	f.write(turndic)
	f.write("\n")
	f.close()