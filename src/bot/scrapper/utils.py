import time
import os
import json
import asyncio
import base64

from dotenv import load_dotenv
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

from bs4 import BeautifulSoup
login_username = os.getenv("LOGIN_USERNAME")
login_password = os.getenv("LOGIN_PASSWORD")
admin_id = os.getenv("ADMIN_ID")
dates_week_class_names = [".fc-mon", ".fc-tue", ".fc-wed",
                          ".fc-thu", ".fc-fri", ".fc-sat"]
left_css_day = ["60px", "174px", "287px", "400px", "513px", "626px"]


def fill_input_by_id(id, input, driver):
    input_field = driver.find_element(By.ID, id)
    input_field.clear()
    input_field.send_keys(input)


def login(username, password, driver):
    driver.find_element("css selector", ".btn-lg").click()
    fill_input_by_id("username", username, driver)
    fill_input_by_id("password", password, driver)

    driver.find_element("css selector", ".input_submit").click()


def go_to_marks_page(driver):
    driver.get("https://myges.fr/student/marks")


def go_to_planning_page(driver):
    driver.get("https://myges.fr/student/planning-calendar")


def extract_html(driver):
    return driver.page_source


async def run_scraper(discord_user, download_dir, marks_collection, planning_collection, users_collection):
    print("Starting scraping...")

    driver = setup_selenium_driver(download_dir)
    user = users_collection.find_one({"user_discord_id": discord_user.id})
    if user and 'username' in user:
        print("username found")
    else:
        print("Username not found.")
    username = user['username']

    password = user['password']

    # Decode the Base64 string
    base64_password = base64.b64decode(password)

    # Convert the decoded bytes to a string
    decoded_password = base64_password.decode()
    url = "https://myges.fr/#/"
    driver.get(url)
    time.sleep(1)

    login(username, decoded_password, driver)
    print("Logged in successfully.")
    # marks
    go_to_marks_page(driver)

    print("Navigated to marks page.")

    html = extract_html(driver)
    json_marks = get_marks(html)

    insert_marks(json_marks, marks_collection, discord_user)

    # planning
    # Run blocking functions in separate threads
    await asyncio.to_thread(go_to_planning_page, driver)
    while not driver.find_element("id", "calendar:j_idt162").is_displayed():
        await asyncio.sleep(1)
    while True:
        try:
            driver.find_element("css selector", ".fc-event")
            break
        except Exception:
            await asyncio.to_thread(driver.find_element("id", "calendar:nextMonth").click)
            while driver.find_element("id", "j_idt10:mgLoadingBar").is_displayed():
                await asyncio.sleep(1)

    html = extract_html(driver)
    event_details = click_events(driver)
    json_data = json.dumps(event_details, indent=2, ensure_ascii=False)
    insert_planning(json_data, planning_collection, discord_user)

    print("Scraping completed.")
    driver.quit()


def get_event_details(driver, events_details, event_date):
    html = extract_html(driver)
    soup = BeautifulSoup(html, 'html.parser')
    # Extract the desired information using CSS selectors or element IDs
    duration = soup.select_one('#duration').text.strip()
    matiere = soup.select_one('#matiere').text.strip()
    intervenant = soup.select_one('#intervenant').text.strip()
    salle = soup.select_one('#salle').text.strip()
    type_ = soup.select_one('#type').text.strip()
    modalite = soup.select_one('#modality').text.strip()

    event_data = {
        "duration": duration,
        "matiere": matiere,
        "intervenant": intervenant,
        "salle": salle,
        "type": type_,
        "modalite": modalite,
        "date": event_date
    }

    events_details.append(event_data)


def click_events(driver):
    events = driver.find_elements("css selector", ".fc-event")
    close_icon = driver.find_element("css selector", ".ui-icon-closethick")
    dates = {}

    dates_week_class_names = [".fc-mon", ".fc-tue", ".fc-wed",
                              ".fc-thu", ".fc-fri", ".fc-sat"]
    left_css_day = ["60px", "174px", "287px", "400px", "513px", "626px"]
    css_to_date = {}

 # Loop over the CSS selectors and left CSS values
    for i, selector in enumerate(dates_week_class_names):
        element = driver.find_element("css selector", selector)
        text = element.text
        left = left_css_day[i]
        css_to_date[left] = text

    events_details = []
    for event in events:
        event_left_property = event.value_of_css_property("left")
        event_date = css_to_date[event_left_property]
        event.click()
        get_event_details(driver, events_details, event_date)
        close_icon.click()
    return events_details


def get_to_working_week(html):
    soup = BeautifulSoup(html, 'html.parser')
    event_container = soup.find('div', {'id': 'calendar:myschedule_container'})
    event_elements = event_container.find_all('div', {'class': 'fc-event'})

    for event_element in event_elements:

        event_time = event_element.find('div', {'class': 'fc-event-time'}).text
        event_title = event_element.find(
            'div', {'class': 'fc-event-title'}).text

        print('Event Time:', event_time)
        print('Event Title:', event_title)
        print('---')


def get_marks(html):
    soup = BeautifulSoup(html, features="html.parser")
    # print(soup)
    # Find the table containing the data
    # table = soup.find('div', id='marksForm:marksWidget:coursesTable')
    data = []
    table = soup.find('table', attrs={"role": "grid"})

    for row in table.tbody.find_all('tr'):
        cells = row.find_all('td')
        matiere = cells[0].text.strip()
        intervenant = cells[1].text.strip()
        coef = cells[2].text.strip()
        ects = cells[3].text.strip()
        cc1 = cells[4].text.strip()
        cc2 = cells[5].text.strip()
        exam = cells[6].text.strip()
        cc1 = cc1.replace(',', '.') if cc1 else None
        cc2 = cc2.replace(',', '.') if cc2 else None
        exam = exam.replace(',', '.') if exam else None
        row_data = {
            "matiere": matiere,
            "intervenant": intervenant,
            "coef": float(coef) if coef else None,
            "ects": float(ects) if ects else None,
            "cc1": float(cc1) if cc1 else None,
            "cc2": float(cc2) if cc2 else None,
            "exam": float(exam) if exam else None
        }
        data.append(row_data)
    json_data = json.dumps(data, indent=2, ensure_ascii=False)
    return json_data


def setup_selenium_driver(download_dir):
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

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
    driver = webdriver.Firefox(service=service, options=options)
    driver.maximize_window()  # Make the browser window fullscreen

    return driver


def insert_marks(json_string, collection, user):
    try:
        json_data = json.loads(json_string)
        documents = []
        inserted_count = 0
        updated_count = 0

        for item in json_data:
            # Process and transform each item into a dictionary format
            document = {
                'user': user.name,
                'matiere': item['matiere'],
                'intervenant': item['intervenant'],
                'coef': item['coef'],
                'ects': item['ects'],
                'cc1': item['cc1'],
                'cc2': item['cc2'],
                'exam': item['exam'],
                'user_discord_id': user.id
            }
            documents.append(document)
            query = {'user_discord_id': user.id, 'matiere': item['matiere']}

            result = collection.update_one(
                query, {'$set': document}, upsert=True)
            if result.upserted_id is not None:
                inserted_count += 1
            else:
                updated_count += 1

        print("Documents inserted:", inserted_count)
        print("Documents updated:", updated_count)

    except Exception as e:
        print(f"Error inserting documents: {str(e)}")


def insert_planning(json_string, collection, user):
    try:
        json_data = json.loads(json_string)
        documents = []
        inserted_count = 0
        updated_count = 0
        for item in json_data:
            # Process and transform each item into a dictionary format
            document = {
                'user': user.name,
                'duration': item['duration'],
                'matiere': item['matiere'],
                'intervenant': item['intervenant'],
                'salle': item['salle'],
                'type': item['type'],
                'modalite': item['modalite'],
                'date': item['date'],
                'user_discord_id': user.id
            }
            documents.append(document)
            query = {'user_discord_id':
                     user.id, 'matiere': item['matiere'], 'date': item['date'], 'duration': item['duration']}

            result = collection.update_one(
                query, {'$set': document}, upsert=True)
            if result.upserted_id is not None:
                inserted_count += 1
            else:
                updated_count += 1

        print("Documents inserted:", inserted_count)
        print("Documents updated:", updated_count)

    except Exception as e:
        print(f"Error inserting documents: {str(e)}")
