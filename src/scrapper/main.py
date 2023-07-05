import time
import os
from dotenv import load_dotenv
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

from pymongo import MongoClient

from utils import login, extract_html, go_to_marks_page, parse_all_links, get_marks, insert_documents


load_dotenv()
mongo_db_key = os.getenv("MONGO_DB_KEY")
username = os.getenv("LOGIN_USERNAME")
password = os.getenv("LOGIN_PASSWORD")
client_mongo = MongoClient(mongo_db_key)
db = client_mongo["myGES"]
users_collection = db["marks_test"]
# Define directory for downloaded images
download_dir = os.path.join(os.getcwd(), 'src/scrapper/json')

if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# Set up Selenium driver
options = webdriver.FirefoxOptions()
# options.headless = True
# profile = webdriver.FirefoxProfile(
#     os.getenv("FIREFOX_PROFILE_PATH"))


# profile.set_preference("browser.download.folderList", 2)
# profile.set_preference("browser.download.manager.showWhenStarting", False)
# profile.set_preference("browser.download.dir", download_dir)
# profile.set_preference(
#     "browser.helperApps.neverAsk.saveToDisk", "image/jpeg,image/png")
service = Service("geckodriver.exe")
# driver = webdriver.Firefox(
#     service=service, options=options, firefox_profile=profile)
driver = webdriver.Firefox(
    service=service, options=options)

url = "https://myges.fr/#/"


driver.get(url)
time.sleep(5)

login(username, password, driver)
go_to_marks_page(driver)
html = extract_html(driver)
json = get_marks(html)

# Pass the JSON string and the MongoDB collection to the function
user = 'paschyz'
insert_documents(json, users_collection, user)
time.sleep(5)
driver.quit()
