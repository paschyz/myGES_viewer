import time
import os
import json

from dotenv import load_dotenv
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

from bs4 import BeautifulSoup


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


def extract_html(driver):
    return driver.page_source


def parse_all_links(html):
    if html:
        # Create a BeautifulSoup object
        soup = BeautifulSoup(html, 'html.parser')

        # Extract specific elements from the HTML using Beautiful Soup methods
        # For example, let's extract all the links on the page
        links = soup.find_all('a')

        # Print the URLs of the links
        for link in links:
            print(link.get('href'))
    else:
        print("HTML source code is empty or None.")


def get_marks(html):
    soup = BeautifulSoup(html, features="html.parser")
    print(soup)
    # Find the table containing the data
    table = soup.find('table', id='marksForm:marksWidget:coursesTable')

    if table:
        # Find all the table rows
        rows = table.find_all('tr')

        # Loop through each row and extract the desired information
        for row in rows:
            # Extract data from each cell
            cells = row.find_all('td')
            subject = cells[0].text.strip()
            instructor = cells[1].text.strip()
            coef = cells[2].text.strip()
            ects = cells[3].text.strip()
            cc1 = cells[4].text.strip()
            cc2 = cells[5].text.strip()
            exam = cells[6].text.strip()

            # Print the extracted information
            print('Subject:', subject)
            print('Instructor:', instructor)
            print('Coef:', coef)
            print('ECTS:', ects)
            print('CC1:', cc1)
            print('CC2:', cc2)
            print('Exam:', exam)
            print('---')
    else:
        print("Table with ID 'marksForm:marksWidget:coursesTable' not found in the HTML.")
