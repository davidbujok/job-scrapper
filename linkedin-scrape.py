from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import re
import requests
import html5lib
import user_credentials


user_login = user_credentials.user_login
user_password = user_credentials.user_password

browser = webdriver.Firefox()
browser.implicitly_wait(3)
browser.get('https://www.linkedin.com')
cookies = [
    {
        "name": "li_at",
        "value": "AQEDAUlKNWIC1XN8AAABjE-MB3wAAAGMc5iLfE4AIkS3JXHBBPgAPuuWMevxxFMDlsxom4Qbll2acKDdF-Hx0u6IHrKrCuRDlLWAO_VyT5ZPiMKsZKetJPf_z6TjSjFTQ9ZXspNg8kw0VmP4-ZS1SLHH",
    },
    {
        "name": "li_gc",
        "value": "MTswOzE3MDIxNDE1OTM7MjswMjGBO8XkeI3WVKUirzwsFUy6vawrBZoWY9sAHJJzMSfrlw==",
    },
    {
        "name": "li_mc",
        "value": "MTsyMTsxNzAyMTQzNTIxOzI7MDIxXXGdJ0jg+IREcWCTVFbEgxKWJFPLpNj2qo5Vgj09xcs=",
    },
    {
        "name": "sdsc",
        "value": "22%3A1%2C1702143370468%7EJAPP%2C0grPpdDIHXYf6fG5jeswsACnKcbw%3D",
    },
    {
        "name": "li_theme", 
        "value": "dark",
    }
]
for cookie in cookies:
    browser.add_cookie( cookie )
    time.sleep(1)
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
job_title_input = browser.find_element(By.XPATH, '//input[starts-with(@id, "jobs-search-box-keyword-id")]')
job_title_input.send_keys('Junior Software Developer')
job_location_input = browser.find_element(By.XPATH,'//input[starts-with(@id, "jobs-search-box-location-id")]')
job_location_input.send_keys('Edinburgh')
time.sleep(3)
job_location_input.send_keys(Keys.ENTER)


# NARROW LIST OF ALL JOBS FOR THE QUERY TO LAST 24h
time_range_selection =  browser.find_element(By.ID, 'searchFilter_timePostedRange')
show_results_button = None
while show_results_button is None:
    try:
        time.sleep(1)
        time_range_selection.click()
        time.sleep(2)
        time_range_24h = browser.find_element(By.ID, 'timePostedRange-r86400')
        time.sleep(1)
        browser.execute_script("arguments[0].click();", time_range_24h)
        time.sleep(3)
        show_results_button = browser.find_element(By.XPATH, '//button[contains(@class, "artdeco-button--primary") and contains(@class, "ember-view") and contains(@class, "ml2") and contains(@class, "artdeco-button") and contains(@class, "artdeco-button--2") and starts-with(@aria-label, "Apply current filter")]')
    except StaleElementReferenceException:
        pass

time.sleep(2)
browser.execute_script("arguments[0].click();", show_results_button)
# show_results_button.click()
# show_results_button = browser.find_element(By.CSS_SELECTOR, 'button[data-control-name="filter_show_results"]')

time.sleep(3)
ul_query_jobs = browser.find_element(By.CLASS_NAME, 'scaffold-layout__list-container')
list_of_jobs = ul_query_jobs.find_elements(By.CLASS_NAME, 'jobs-search-results__list-item')

jobs_file_txt = open("job_offers.txt", "w")
for job in list_of_jobs:
    job.click()
    time.sleep(3)
    job_title = browser.find_element(By.CLASS_NAME, 'job-details-jobs-unified-top-card__job-title-link').text
    print(job_title)
    jobs_file_txt.write(f"{ job_title } \n")
    job_header_info = browser.find_element(By.CLASS_NAME, 'job-details-jobs-unified-top-card__primary-description-container').text
    print(job_header_info)
    jobs_file_txt.write(f"{ job_header_info } \n")
    job_header_level = browser.find_element(By.CLASS_NAME, 'job-details-jobs-unified-top-card__job-insight').text
    print(job_header_level)
    jobs_file_txt.write(f"{ job_header_level } \n")
    job_about = browser.find_element(By.ID, 'job-details').text
    jobs_file_txt.write(f"{ job_about } \n")
    jobs_file_txt.write(f"---------------------------------------------------------------------------------------------------- \n")



