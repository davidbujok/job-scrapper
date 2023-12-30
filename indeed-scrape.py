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
from helpers import get_url_id, parse_indeed_realtive_date_to_date_object, parsed_date_to_python_date_object, cut_out_company, get_id_indded_job

browser = webdriver.Firefox()
browser.implicitly_wait(3)

job_title_text = None
job_location_text = None
job_description = None
company_name_text = None
link_to_job = None
job_header_level = None
ad_date = None

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

# TIME RANGE SELECTION , SWITCH OFF FOR TESTING 
# time.sleep(2)
# time_range_selection_button = browser.find_element(
#     By.ID, "filter-dateposted"
# )
# browser.execute_script("arguments[0].click();", time_range_selection_button)
# time.sleep(1)
# hours_24 = browser.find_element(By.ID, 'filter-dateposted-menu')
# hours_24_link = hours_24.find_elements(By.TAG_NAME, 'a')
# hours_24_link[0].click()

time.sleep(1.5)

try:
    div_block_of_job_cards = browser.find_element(By.ID, 'mosaic-provider-jobcards')
except NoSuchElementException:
    print('No new jobs found, exiting execution')
    sys.exit()

ul_of_job_cards = div_block_of_job_cards.find_element(By.TAG_NAME, 'ul')
list_of_li_jobs = ul_of_job_cards.find_elements(By.TAG_NAME, 'li')


try:
    with connection.cursor() as cursor:
        query_id = "SELECT id FROM websites WHERE name = 'indeed'"
        id_of_the_website = None
        try:
            cursor.execute(query_id)
            id_of_the_website = cursor.fetchone()
        except Exception as e:
            print(f"Error executing select query: {e}")

        for job_card in list_of_li_jobs:
            try:
                browser.execute_script("arguments[0].scrollIntoView(true);", job_card)
                time.sleep(1)
                a_href_link = job_card.find_element(By.TAG_NAME, 'a')
                relative_post_date = job_card.find_element(By.CLASS_NAME, 'date').text
                ad_date = parse_indeed_realtive_date_to_date_object(relative_post_date)
                link_to_job = a_href_link.get_attribute('href')
                a_href_link.click()
                classes_with_id = job_card.find_element(By.TAG_NAME, 'div').get_attribute('class')
                job_id = get_id_indded_job(classes_with_id)
                # __AUTO_GENERATED_PRINT_VAR_START__
                print(f" job_id: {str(job_id)}") # __AUTO_GENERATED_PRINT_VAR_END__
                job_header = browser.find_element(By.XPATH,
                                                  '//div[contains(@class, "jobsearch-HeaderContainer")]')
                company_name_text = browser.find_element(By.CSS_SELECTOR,
                                                    '[data-company-name="true"]').text
                job_description = browser.find_element(By.ID, 'jobDescriptionText').text
                job_title_text = job_header.find_element(By.TAG_NAME, 'h2').text
                job_location_text = browser.find_element(
                    By.CSS_SELECTOR, '[data-testid="inlineHeader-companyLocation"]'
                ).text

                time.sleep(1)
            except NoSuchElementException:
                print('Not a link card')
            except ElementNotInteractableException:
                print('Not in a view')

            time.sleep(1)

            try:
                cursor.execute(
                    "INSERT INTO jobs (url, job_id, position, company, location, level, about, post_date, websites_id) \
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);",
                    (
                        link_to_job,
                        job_id,
                        job_title_text,
                        company_name_text,
                        job_location_text,
                        job_header_level,
                        job_description,
                        ad_date,
                        id_of_the_website,
                    ),
                )
            except errors.UniqueViolation:
                print('Job already exist in the database')
                pass
            cursor.connection.commit()
except errors.ExternalRoutineException as e:
    print(e)
