from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime
from dateutil import tz
import json
import os
from config import config 
import tweepy 

def twitter_auth(api_key,api_secret,acess_token,access_secret):
    auth = tweepy.OAuthHandler(api_key,api_secret)
    auth.set_access_token(acess_token,access_secret)
    api = tweepy.API(auth)
    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")
    return auth, api

def get_chrome():
    options = Options()
    options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-dev-shm-usage")

    return webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),options=options)

def scraper(driver):
    scraped_data={}
    driver.implicitly_wait(20)
    
    driver.get("https://stats.synthetix.io/")
    time.sleep(config.page_load_waiting)

    with open("config/object_list.json", "r") as read_file:
        data = json.load(read_file)
    
    for i in data:
        scraped_data[i]=driver.find_element(By.XPATH,data[i]).text.replace("$","")
    
    return scraped_data

def get_snx_staked_percent(data):
    snx_staked=int(data["total_snx_staked"].replace(",",""))
    marcet_cap=int(data["snx_marcet_cap"].replace(",",""))
    return float("{0:.2f}".format((snx_staked/marcet_cap)*100))

def twitt_prepare(data):
    tzlocal = tz.tzoffset('IST', 0)
    time_mark="\n\n"+str(datetime.now(tz=tzlocal).date()).replace("-","/")+" "+str(datetime.now(tz=tzlocal).time()).split(".")[:-1][0]+" UTC"

    if datetime.isoweekday(datetime.now(tz=tzlocal)) == config.weekly_twitt_day and datetime.now(tz=tzlocal).hour == config.weekly_twitt_hour:
        tamplate_file=open(config.weekly_twitt_template_patch,"rt")
        tamplate=tamplate_file.read()
        tamplate_file.close()
        twitt=tamplate.format(**data)
        twitt+=time_mark
        return twitt 
    
    else:
        tamplate_file=open(config.hourly_twitt_template_patch,"rt")
        tamplate=tamplate_file.read()
        tamplate_file.close()
        twitt=tamplate.format(**data)
        twitt+=time_mark
        return twitt 

if __name__ == "__main__":
    auth,api=twitter_auth(config.consumer_key,config.consumer_secret,config.acess_token,config.access_secret)
    try:
        chrome=get_chrome()
        while True:
            try:
                data=scraper(chrome)
                data["snx_staked_percent"]=get_snx_staked_percent(data)
                twitt=twitt_prepare(data)
                print(twitt)
                api.update_status(twitt)
                print("successfully published ")
                time.sleep(3600-config.page_load_waiting)
            except Exception as e:
                break
    
    finally:
        print("bot stop...")
        if chrome is not None:
            chrome.quit()
        print("bot stopped")