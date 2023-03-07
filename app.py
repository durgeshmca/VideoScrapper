from flask import Flask,render_template,redirect,request,Response,url_for
from flask_cors import CORS,cross_origin
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import csv
import logging
logging.basicConfig(filename="scrapper.log" , level=logging.INFO)

app = Flask(__name__)

@cross_origin()
@app.route("/")
def home():
    return render_template("index.html")

@cross_origin()
@app.route("/scrap",methods=['POST']) 
def scrap_data():
    try :

        url = request.form.get("content")
        ser = Service(r"/official/official_docs/PythonLerning/VideoScrapper/driver/geckodriver")
        option = webdriver.FirefoxOptions()
        driver = webdriver.Firefox(service=ser, options=option)
        driver.maximize_window()
        driver.get(url)
        # baseUrl = "https://youtube.com/"
        vedioList = driver.find_elements(By.XPATH,"//a[@id='thumbnail']")
        imageList = driver.find_elements(By.XPATH, "//a[@id='thumbnail']/yt-image/img")
        titles = driver.find_elements(By.ID,'video-title-link')
        ls = driver.find_elements(By.XPATH,"//div[@id='metadata-line']")
        del vedioList[0]
        scrapData = []
        with open('youtube_scrap.csv','w') as fp:
            csv_writer = csv.writer(fp)
            header = ["S.No","Video URL","Thumbnails URL","Title","Views","Posted at"]
            csv_writer.writerow(header)

            for i in range(5):
                vurl = str(vedioList[i].get_attribute('href'))
                imgUrl = imageList[i].get_attribute('src')
                title = titles[i].text
                txt = ls[0].text
                view, post_time = txt.split("\n")
                data = [i+1,vurl,imgUrl,title,view,post_time]
                scrapData.append({
                    "index" : i+1,
                    "vurl": vurl,
                    "turl": imgUrl,
                    "title" : title,
                    "views" : view,
                    "time" : post_time
                })
                csv_writer.writerow(data)
            



        driver.close()
        return render_template("result.html",scrapData = scrapData)
    except Exception as e:
        logging.info(e)
        return "Error:"+ e
if __name__=="__main__":
    app.run(host="0.0.0.0")
