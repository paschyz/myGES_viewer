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

from utils import *


load_dotenv()
mongo_db_key = os.getenv("MONGO_DB_KEY")
username = os.getenv("LOGIN_USERNAME")
password = os.getenv("LOGIN_PASSWORD")
client_mongo = MongoClient(mongo_db_key)
db = client_mongo["myGES"]
marks_collection = db["marks"]
planning_collection = db["planning"]
# Define directory for downloaded images
download_dir = os.path.join(os.getcwd(), 'src/scrapper/json')
run_scraper(username, password, download_dir)
