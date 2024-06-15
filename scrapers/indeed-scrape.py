import psycopg2
import sys
from psycopg2 import Error, errors
from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotInteractableException,
    StaleElementReferenceException
)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

from sqlalchemy import column, table
from helpers import (
    parse_indeed_realtive_date_to_date_object,
    get_id_indded_job
)

browser = webdriver.Firefox()
browser.implicitly_wait(3)

job_title_text = None
job_location_text = None
job_description_text = None
company_name_text = None
link_to_job = None
job_header_level = None
ad_date = None
job_id = None

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

print("What job you're looking for?")
# job_title_text = input()
job_title_text = ""
print("Where?")
# job_location = input()
job_location = "Dunfermline, Fife"
time.sleep(1)
try:
    ad_alert = browser.find_element(By.XPATH, '//button[contains(@aria-label,"close")]')
    ad_alert.click()
except NoSuchElementException:
    print('No add popup')

def find_and_fill_inputs(searched_job_title_text, searched_job_location):
    time.sleep(2)
    job_title_text_input_element = browser.find_element(
        By.XPATH, '//input[starts-with(@id, "text-input-what")]'
    )
    job_title_text_input_element.send_keys(searched_job_title_text)

    job_location_input_element = browser.find_element(
        By.XPATH, '//input[starts-with(@id, "text-input-where")]'
    )
    job_location_input_element.send_keys(searched_job_location)

    time.sleep(1)
    job_location_input_element.send_keys(Keys.ENTER)

find_and_fill_inputs(job_title_text, job_location)

# TIME RANGE SELECTION , SWITCH OFF FOR TESTING 
time.sleep(2)
time_range_selection_button = browser.find_element(
    By.ID, "filter-dateposted"
)
browser.execute_script("arguments[0].click();", time_range_selection_button)
time.sleep(1)
hours_24 = browser.find_element(By.ID, 'filter-dateposted-menu')
hours_24_link = hours_24.find_elements(By.TAG_NAME, 'a')
# 0 - 24hrs | 1 - 3 days | 2 - 7 days | 3 - 14 days
hours_24_link[2].click()
time.sleep(1.5)

try:
    ad_alert = browser.find_element(By.XPATH, '//button[contains(@aria-label,"close")]')
    ad_alert.click()
except NoSuchElementException:
    print('No add popup')
time.sleep(0.5)

try:
    div_block_of_job_cards = browser.find_element(By.ID, 'mosaic-provider-jobcards')
except NoSuchElementException:
    print('No new jobs found, exiting execution')
    sys.exit()

ul_of_job_cards = div_block_of_job_cards.find_element(By.TAG_NAME, 'ul')
# print(ul_of_job_cards.get_attribute('class'))
# ./li this allow to search only li(s) directly under the tag
list_of_li_jobs = ul_of_job_cards.find_elements(By.XPATH, './li')


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
                # browser.execute_script("arguments[0].scrollIntoView(true);", job_card)
                time.sleep(1)
                card_outline = job_card.find_element(By.XPATH, './div[1]')
                card_outline.click()

                job_title = browser.find_element(By.CLASS_NAME, "jobsearch-JobInfoHeader-title")
                job_title_text = job_title.text
                print(job_title.text)

                link_to_job = str(browser.current_url)
                print(link_to_job)

                company_name_and_location_div = job_card.find_element(By.CLASS_NAME, "company_location")
                company_name = company_name_and_location_div.find_element(By.TAG_NAME, 'span')
                company_name_text = company_name.text
                print(company_name_text) 

                company_location = company_name_and_location_div.find_element(By.CSS_SELECTOR,
                                                                              'div[data-testid="text-location"]')
                job_location_text = company_location.text
                print(company_location.text)

                job_description = browser.find_element(By.ID, 'jobDescriptionText') 
                job_description_text = job_description.text
                # print(job_description.text)

                post_date = parse_indeed_realtive_date_to_date_object(job_card.text)
                ad_date = post_date
                print(post_date)
                # company_name_and_location_div_lev_2 = company_name_and_location_div.find_element(By.TAG_NAME, 'div')
                # company_name_and_location_basket = company_name_and_location_div_lev_2.find_elements(By.TAG_NAME, 'div')

                # div_container = card_outline.find_element(By.XPATH, './div[1]')
                # div_container_nest_lev_1 = div_container.find_element(By.XPATH, './div[1]')
                # div_container_nest_lev_2 = div_container_nest_lev_1.find_element(By.XPATH, './div[1]')
                # div_beacon = div_container_nest_lev_2.find_element(By.XPATH, './div[1]')
                # bottom_table = div_beacon.find_element(By.XPATH, './table[2]')
                # print(bottom_table.text)
                # span = bottom_table.find_element(By.XPATH, './/span[@data-testid="myJobsStateDate"]')
                # direct_date = browser.execute_script("""
                #     var parent = arguments[0];
                #     var child = parent.firstChild;
                #     var textContent = '';
                #     while(child) {
                #         if (child.nodeType === Node.TEXT_NODE) {
                #             textContent += child.textContent;
                #         }
                #         child = child.nextSibling;
                #     }
                #     return textContent;
                # """, span)
                #
                # ad_date = parse_indeed_realtive_date_to_date_object(direct_date)
                # # print("ad date: ", ad_date)
                #
                # top_table = div_beacon.find_element(By.XPATH, './table[1]')
                # table_body = top_table.find_element(By.TAG_NAME, 'tbody')
                # tr_element = table_body.find_element(By.TAG_NAME, 'tr')
                # td_element = tr_element.find_element(By.TAG_NAME, 'td')
                # job_title_div = tr_element.find_element(By.TAG_NAME, 'div')
                # job_title_text = job_title_div.text
                # heading_with_link = job_title_div.find_element(By.TAG_NAME, 'h2')
                # link_tag = heading_with_link.find_element(By.TAG_NAME, 'a')
                # link_to_job = link_tag.get_attribute('href')
                # # print(link_to_job)
                # job_id = link_tag.get_property('id')
                # company_div = td_element.find_element(By.XPATH, './div[2]')
                # company_nested_div = company_div.find_element(By.TAG_NAME, 'div')
                # company_location_div = company_nested_div.find_element(By.TAG_NAME, 'div')
                # job_location_text = company_location_div.text
                # company_nested_div_content = company_nested_div.text.splitlines()
                # company_name_text = "";
                # if len(company_nested_div_content) > 0 :
                #     company_name_text = company_nested_div_content[0]
                #     # print(company_name_text)
                #
                # job_details_block = browser.find_element(By.XPATH, 
                #     '//div[contains(@class, "jobsearch-RightPane")]')
                # job_full_details_block = job_details_block.find_element(By.TAG_NAME,
                #     'div')
                # details_block_div_nested_levOne = job_full_details_block.find_element(By.TAG_NAME,
                #                                                                       'div')
                # div_nested_levTwo = browser.find_element(By.XPATH, 
                #     '//div[contains(@class, "fastviewjob")]')
                # div_nested_levThree = div_nested_levTwo.find_element(By.XPATH, 
                #     '//div[contains(@class, "jobsearch-JobComponent")]')
                # div_nested_levFour = div_nested_levTwo.find_element(By.XPATH, 
                #     '//div[contains(@class, "jobsearch-embeddedBody")]')
                # job_description = div_nested_levFour.find_element(By.ID, 
                #     'jobDescriptionText')
                # job_description_text = job_description.text
                
            except NoSuchElementException:
                print('Not a link card')
            except ElementNotInteractableException:
                print('Not in a view')
            except StaleElementReferenceException:
                print('Dom element not in a node tree anymore')

            time.sleep(1)
            apply_status = False

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
                )
                sql = """
INSERT INTO jobs (url, job_id, position, company, location, level, about, post_date, websites_id, apply_status)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
RETURNING position, company;
"""
                data = (link_to_job, job_id, job_title_text, company_name_text, job_location_text,
                        job_title_text, job_description_text, ad_date, id_of_the_website, apply_status)
                cursor.execute(sql, data)
            except errors.UniqueViolation:
                print('Job already exist in the database')
                pass
            except errors.NotNullViolation:
                print('Missing field')
                pass
            print('Job added to database')
            cursor.connection.commit()
except errors.ExternalRoutineException as e:
    print(e)
