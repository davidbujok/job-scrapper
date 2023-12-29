import psycopg2
import sys
from psycopg2 import Error, errors
from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    ElementNotInteractableException
)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from helpers import get_url_id, parsed_date_to_python_date_object, cut_out_company, cut_out_location

browser = webdriver.Firefox()
browser.implicitly_wait(3)

try:
    browser.get("https://uk.indeed.com/")
except Exception:
    print("Site can't be reached, ", {Exception})

connection = psycopg2.connect(
    database="mydatabase", host="localhost", user="arch", password="", port=5432
)

try:
    with connection.cursor() as cursor:
        try:
            website_url = str(browser.current_url)
            cursor.execute(
                "INSERT INTO websites (name, url) VALUES ('indeed', %s);",
                (website_url,),
            )
            connection.commit()
        except Exception as e:
            connection.rollback()
            print(f"Error inserting into websites table: {e}")
except Error as e:
    print("Database connection error: ", e)


# JOB TITLE AND LOCATION OF THE QUERY

print("What job you're looking for?")
job_title = 'Junior Software Edinburgh'
print("Where?")
job_location = 'Edinburgh'


def find_and_fill_inputs(searched_job_title, searched_job_location):
    time.sleep(2)
    job_title_input_element = browser.find_element(
        By.XPATH, '//input[starts-with(@id, "text-input-what")]'
    )
    job_title_input_element.send_keys(searched_job_title)

    job_location_input_element = browser.find_element(
        By.XPATH, '//input[starts-with(@id, "text-input-where")]'
    )
    job_location_input_element.send_keys(searched_job_location)

    time.sleep(1)
    job_location_input_element.send_keys(Keys.ENTER)

find_and_fill_inputs(job_title, job_location)

time.sleep(2)
time_range_selection_button = browser.find_element(
    By.ID, "filter-dateposted"
)
browser.execute_script("arguments[0].click();", time_range_selection_button)
time.sleep(1)
hours_24 = browser.find_element(By.ID, 'filter-dateposted-menu')
hours_24_link = hours_24.find_elements(By.TAG_NAME, 'a')
hours_24_link[0].click()

time.sleep(2)
try:
    div_block_of_job_cards = browser.find_element(By.ID, 'mosaic-provider-jobcards')
except NoSuchElementException:
    print('No new jobs found, exiting execution')
    sys.exit()

ul_of_job_cards = div_block_of_job_cards.find_element(By.TAG_NAME, 'ul')
list_of_li_jobs = ul_of_job_cards.find_elements(By.TAG_NAME, 'li')

for job_card in list_of_li_jobs:
    try:
        browser.execute_script("arguments[0].scrollIntoView(true);", job_card)
        time.sleep(1)
        a_href_link = job_card.find_element(By.TAG_NAME, 'a')
        link_to_job = a_href_link.get_attribute('href')
        a_href_link.click()
        print(job_card.text) 
        time.sleep(1)
    except NoSuchElementException:
        print('Not a link card')
    except ElementNotInteractableException:
        print('Not in a view')

    time.sleep(1)
# list_of_jobs = select_div_query_jobs.find_elements(
#     By.CLASS_NAME, "jobs-search-results__list-item"
# )

# for job in list_of_jobs:
#     job.click()
#     job_link = browser.current_url
#     print(job_link)

# try:
#     with connection.cursor() as cursor:
#         query_id = "SELECT id FROM websites WHERE name = 'indeed'"
#         id_of_the_website = None
#         try:
#             cursor.execute(query_id)
#             id_of_the_website = cursor.fetchone()
#         except Exception as e:
#             print(f"Error executing select query: {e}")

#         for job in list_of_jobs:
#             job.click()
#             job_link = browser.current_url
#             print(job_link)
#             time.sleep(3)
#             job_title = browser.find_element(
#                 By.CLASS_NAME, "job-details-jobs-unified-top-card__job-title-link"
#             ).text
#             job_header_info = browser.find_element(
#                 By.CLASS_NAME,
#                 "job-details-jobs-unified-top-card__primary-description-container",
#             ).text
#             job_header_level = browser.find_element(
#                 By.CLASS_NAME, "job-details-jobs-unified-top-card__job-insight"
#             ).text
#             job_about = browser.find_element(By.ID, "job-details").text
#             job_id = get_url_id(job_link)
#             location = cut_out_location(job_header_info)
#             company = cut_out_company(job_header_info)
#             ad_date = parsed_date_to_python_date_object(job_header_info)
#             try:
#                 cursor.execute(
#                     "INSERT INTO jobs (url, job_id, position, company, location, level, about, post_date, websites_id) \
#                                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);",
#                     (
#                         job_link,
#                         job_id,
#                         job_title,
#                         company,
#                         location,
#                         job_header_level,
#                         job_about,
#                         ad_date,
#                         id_of_the_website,
#                     ),
#                 )
#             except errors.UniqueViolation:
#                 print('Job already exist in the database')
#                 pass
#             cursor.connection.commit()
# except errors.ExternalRoutineException as e:
#     print(e)
