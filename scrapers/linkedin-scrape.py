import sys
import psycopg2
from psycopg2 import Error, errors
from selenium import webdriver
from sqlalchemy import Table, column, insert, table
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from logger import log_job
from helpers import (
    get_url_id,
    parsed_date_to_python_date_object,
    # cut_out_company,
    cut_out_location,
)
import user_credentials
options = webdriver.FirefoxOptions()
options.add_argument("--headless")
browser = webdriver.Firefox(options=options)
browser.implicitly_wait(3)

try:
    browser.get("https://www.linkedin.com")
except Exception:
    print("Site can't be reached, ", {Exception})

connection = psycopg2.connect(
    database="mydatabase", host="localhost", user="arch", password="", port=5432
)

# try:
#     with connection.cursor() as cursor:
#         try:
#             website_url = str(browser.current_url)
#             cursor.execute(
#                 "INSERT INTO websites (name, url) VALUES ('linkedin', %s);",
#                 (website_url,),
#             )
#             connection.commit()
#         except Exception as e:
#             connection.rollback()
#             print(f"Error inserting into websites table: {e}")
# except Error as e:
#     print("Database connection error: ", e)

try:
    cookies = user_credentials.cookies
    for cookie in cookies:
        browser.add_cookie(cookie)
        time.sleep(1)
    print("Sucesfully injected cookies' to linkedin")
except Error as e:
    cookies = None
    print("Check if cookies in user_credentials are valid")


if cookies == None:
    print("Missing Cookies, you need to add cookies first")
    user_login = user_credentials.user_login
    user_password = user_credentials.user_password
    if user_login or user_password == None:
        print("No credentials provided, you need to add user's credentials first ")
        exit()
    try:
        user_credentials_login = browser.find_element(By.ID, "session_key")
        time.sleep(2)
        user_credentials_login.send_keys(user_login)
        user_credentials_password = browser.find_element(By.ID, "session_password")
        user_credentials_password.send_keys(user_password)
        credential_confirm = browser.find_element(
            By.CSS_SELECTOR, "button.btn-md:nth-child(3)"
        )
        time.sleep(2)
        credential_confirm.click()
    except NoSuchElementException:
        print("You're already loged in")

# JOB TITLE AND LOCATION OF THE QUERY
# This comes from the flask server. Check ../app/controllers/jobs.py [run_script] method
browser.get("https://www.linkedin.com/jobs/")
searched_job_title_text = sys.argv[1]
searched_job_location = sys.argv[2]

# Injecting parameters from Flask app. Input comes from the React App ../job-search/src/Components/ScrapeJobs.tsx
def search_for_jobs(searched_job_title_text, searched_job_location):
    time.sleep(2)
    job_title_text_input_element = browser.find_element(
        By.XPATH, '//input[starts-with(@id, "jobs-search-box-keyword-id")]'
    )

    job_title_text_input_element.send_keys(searched_job_title_text)
    time.sleep(2)

    job_location_input_element = browser.find_element(
        By.XPATH, '//input[starts-with(@id, "jobs-search-box-location-id")]'
    )
    job_location_input_element.send_keys(searched_job_location)
    time.sleep(3)
    job_location_input_element.send_keys(Keys.ENTER)

search_for_jobs(searched_job_title_text, searched_job_location)

# NARROW LIST OF ALL JOBS FOR THE QUERY TO LAST 24H
time_range_selection_button = browser.find_element(
    By.ID, "searchFilter_timePostedRange"
)
time_range_24h = None
while time_range_24h is None:
    try:
        time.sleep(1)
        time_range_selection_button.click()
        time.sleep(2)
        time_range_24h = browser.find_element(By.ID, "timePostedRange-r86400")
        time.sleep(1)
        browser.execute_script("arguments[0].click();", time_range_24h)
        time.sleep(1.75)
    except StaleElementReferenceException:
        print("Waiting for the element to appear")
        pass

# WAIT, AVOID CAPTCHA / BOT DETECTION
time.sleep(1.5)
time_range_selection_button.click()

time.sleep(2.5)
ul_query_jobs = browser.find_element(By.CLASS_NAME, "scaffold-layout__list-container")
list_of_jobs = ul_query_jobs.find_elements(
    By.CLASS_NAME, "jobs-search-results__list-item"
)

try:
    with connection.cursor() as cursor:
        user_login = user_credentials.user_login
        user_password = user_credentials.user_password
        id_of_the_website = None
        query_id = "SELECT id FROM websites WHERE name = 'linkedin'"
        try:
            cursor.execute(query_id)
            id_of_the_website = cursor.fetchone()
        except Exception as e:
            print(f"Error executing select query: {e}")

        for job in list_of_jobs:
            job.click()
            job_link = browser.current_url
            time.sleep(3)
            job_title_text = job.find_element(
                By.CLASS_NAME, "job-card-list__title--link"
            ).text
            job_header_info = browser.find_element(
                By.CLASS_NAME,
                "job-details-jobs-unified-top-card__primary-description-container",
            ).text
            company_element = browser.find_element(
                By.CLASS_NAME,
                "job-details-jobs-unified-top-card__company-name",
            ).text
            # print(job_header_info)
            job_header_level = browser.find_element(
                By.CLASS_NAME, "job-details-jobs-unified-top-card__job-insight"
            ).text
            job_about = browser.find_element(By.ID, "job-details").text
            # print(job_about) 
            job_id = get_url_id(job_link)
            location = cut_out_location(job_header_info)
            # print(f"location {location}")
            company = company_element
            # print(f"company {company}")
            ad_date = parsed_date_to_python_date_object(job_header_info)

            try:
                jobs = table(
                    "jobs",
                    column("level"),
                    column("position"),
                    column("about"),
                    column("url"),
                    column("website_id"),
                    column("job_id"),
                    column("post_date"),
                    column("company"),
                    column("location"),
                    column("apply_status"),
                    column("hidden_status"),
                )
                sql = """
INSERT INTO jobs (url, job_id, position, company, location, level, about, post_date, websites_id,
apply_status, hidden_status)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
RETURNING position, company;
"""
                data = (job_link, job_id, job_title_text, company, location, job_header_level,
                        job_about, ad_date, id_of_the_website, False, False)
                log_job("linkedin", job_title_text, company, location, job_header_level, ad_date)
                cursor.execute(sql, data)
            except errors.UniqueViolation:
                print("Job already exist in the database")
                pass
            cursor.connection.commit()
except errors.ExternalRoutineException as e:
    print(e)
browser.quit()
