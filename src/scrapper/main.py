import time
import os
from dotenv import load_dotenv
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

from utils import login, extract_html, go_to_marks_page, parse_all_links, get_marks


load_dotenv()
username = os.getenv("LOGIN_USERNAME")
password = os.getenv("LOGIN_PASSWORD")

# # Define directory for downloaded images
# download_dir = os.path.join(os.getcwd(), 'images')

# if not os.path.exists(download_dir):
#     os.makedirs(download_dir)

# Set up Selenium driver
options = webdriver.FirefoxOptions()
# options.headless = True
profile = webdriver.FirefoxProfile(
    os.getenv("FIREFOX_PROFILE_PATH"))


profile.set_preference("browser.download.folderList", 2)
profile.set_preference("browser.download.manager.showWhenStarting", False)
# profile.set_preference("browser.download.dir", download_dir)
profile.set_preference(
    "browser.helperApps.neverAsk.saveToDisk", "image/jpeg,image/png")
service = Service("geckodriver.exe")
driver = webdriver.Firefox(
    service=service, options=options, firefox_profile=profile)

# Set up FUTWIZ page URL
url = "https://myges.fr/#/"

# Define function to fill input fields by ID

driver.get(url)

login(username, password, driver)
go_to_marks_page(driver)
html = extract_html(driver)
get_marks(html)

time.sleep(5)
driver.quit()
