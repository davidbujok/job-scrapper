import psycopg2
from psycopg2 import Error, errors
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

from sqlalchemy import except_
import user_credentials

browser = webdriver.Firefox()
browser.implicitly_wait(3)
browser.get('https://www.linkedin.com')

try:
    connection = psycopg2.connect(
        database="mydatabase",
        host="localhost",
        user="arch",
        password="",
        port=5432
    )

    with connection.cursor() as cursor:
        user_login = user_credentials.user_login
        user_password = user_credentials.user_password
        website_url = str(browser.current_url)
        try:
            cursor.execute("INSERT INTO websites (name, url) VALUES ('linkedin', %s);",
                           (website_url,))
            connection.commit()
        except Exception as e:
            connection.rollback()
            print(f"Error inserting into websites table: {e}")

        cookies = user_credentials.cookies
        for cookie in cookies:
            browser.add_cookie(cookie)
            time.sleep(1)


except Error as e:
    print(f"Error connecting to the database: {e}")

# website_title = browser.title

# desired_title = 'LinkedIn'
# desired_title_pattern = rf'\b{re.escape(desired_title)}\b'
# match = re.search(desired_title_pattern, website_title, re.IGNORECASE)

# # Check if the match is found
# assert match is not None, f"The phrase '{desired_title}' is not in the title: '{website_title}'"

# # LOGIN PHASE
# try:
#     user_credentials_login = browser.find_element(By.ID, 'session_key')
#     time.sleep(2)
#     user_credentials_login.send_keys(user_login)
#     user_credentials_password = browser.find_element(By.ID, 'session_password')
#     user_credentials_password.send_keys(user_password)
#     credential_confirm = browser.find_element(By.CSS_SELECTOR, 'button.btn-md:nth-child(3)')
#     time.sleep(2)
#     credential_confirm.click()
# except NoSuchElementException:
#     print("You're alreadu loged in")

# JOB TITLE AND LOCATION OF THE QUERY
time.sleep(2)
browser.get('https://www.linkedin.com/jobs/')
job_title_input = browser.find_element(By.XPATH, 
                                       '//input[starts-with(@id, "jobs-search-box-keyword-id")]')
job_title_input.send_keys('Junior Software Developer')
job_location_input = browser.find_element(By.XPATH,
                                       '//input[starts-with(@id, "jobs-search-box-location-id")]')
job_location_input.send_keys('Edinburgh')
time.sleep(3)
job_location_input.send_keys(Keys.ENTER)

print('Filter time range')

# NARROW LIST OF ALL JOBS FOR THE QUERY TO LAST 24h
time_range_selection =  browser.find_element(By.ID, 'searchFilter_timePostedRange')
time_range_24h = None
while time_range_24h is None:
    try:
        time.sleep(1)
        time_range_selection.click()
        time.sleep(2)
        time_range_24h = browser.find_element(By.ID, 'timePostedRange-r86400')
        time.sleep(1)
        browser.execute_script("arguments[0].click();", time_range_24h)
        time.sleep(1.75)
    except StaleElementReferenceException:
        print('Waiting for the element to appear')
        pass
print("Results filtered to last 24hrs")

time.sleep(1.5)
time_range_selection.click()
# browser.execute_script("arguments[0].click();", show_results_button)
# show_results_button.click()
# show_results_button = browser.find_element(By.CSS_SELECTOR, 
                                        # 'button[data-control-name="filter_show_results"]')

time.sleep(3)
ul_query_jobs = browser.find_element(By.CLASS_NAME, 'scaffold-layout__list-container')
list_of_jobs = ul_query_jobs.find_elements(By.CLASS_NAME, 'jobs-search-results__list-item')
# XPATH exmaple
# show_results_button = browser.find_element(By.XPATH, '//button[contains(@class, "artdeco-button")
# and contains(@class, "ember-view") and contains(@class, "ml2") and
# contains(@class, "artdeco-button--2") and starts-with(@aria-label, "Apply current filter")]')

try:
    connection = psycopg2.connect(
        database="mydatabase",
        host="localhost",
        user="arch",
        password="",
        port=5432
    )

    with connection.cursor() as cursor:
        user_login = user_credentials.user_login
        user_password = user_credentials.user_password
        query_id = "SELECT id FROM websites WHERE name = 'linkedin'"
        id_of_the_website = None
        try:
            cursor.execute(query_id)
            id_of_the_website = cursor.fetchone()
        except Exception as e:
            print(f"Error executing select query: {e}")
            
        for job in list_of_jobs:
            job.click()
            job_link = browser.current_url
            print(job_link)
            time.sleep(3)
            job_title = browser.find_element(By.CLASS_NAME,
                         'job-details-jobs-unified-top-card__job-title-link').text
            job_header_info = browser.find_element(By.CLASS_NAME,
                         'job-details-jobs-unified-top-card__primary-description-container').text
            job_header_level = browser.find_element(By.CLASS_NAME,
                         'job-details-jobs-unified-top-card__job-insight').text
            job_about = browser.find_element(By.ID, 'job-details').text
            cursor.execute("INSERT INTO jobs (url, position, details, level, about, websites_id) \
                            VALUES (%s, %s, %s, %s, %s, %s);",
                           (job_link, job_title, job_header_info, job_header_level, job_about,
                            id_of_the_website))
            cursor.connection.commit()
except errors.ExternalRoutineException as e:
    print(e)
