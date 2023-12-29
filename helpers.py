import re
import psycopg2
from psycopg2.errors import Error
import parsedatetime
import datetime

connection = psycopg2.connect(
    database="mydatabase", host="localhost", user="arch", password="", port=5432
)

selected_id = 64
find_job_position_by_id_query = 'SELECT * FROM jobs WHERE id = %s'
job_id = None
job_details = None
try:
    with connection.cursor() as cursor:
        try:
            job_data = cursor.execute(find_job_position_by_id_query, ( selected_id, ))
            job_id = cursor.fetchall()
            # print(job_id[0][1])
            # print(job_id[0][2])
            # print(job_id[0][3])
            # print(job_id[0][4])
            # print(job_id[0][5])
            job_details = job_id[0][3]

        except Exception as e:
            connection.rollback()
            print(f"Error inserting into websites table: {e}")
except Error as e:
    print("Database connection error: ", e)


def get_url_id(web_url):
    job_id_pattern = re.compile(r'currentJobId=([^&]+)')
    job_id_match = re.search(job_id_pattern, web_url)
    if job_id_match is not None:
        extracted_id = job_id_match.group(1)
        return extracted_id

def cut_out_company(job_details):
    company_pattern = re.compile(r'([^·]+)')
    comapny = re.search(company_pattern, job_details) 
    if comapny is not None:
        extracted_company = comapny.group(1)
        return extracted_company 

# if job_details is not None:
#     print(cut_out_company(job_details))

def cut_out_location(job_details):
    location_pattern = re.compile(r'(?<=\·)(.*?Kingdom)')
    location = re.search(location_pattern, job_details) 
    if location is not None:
        extracted_location = location.group(1)
        return extracted_location

def cut_out_time(job_details):
    time_pattern = re.compile(r'(\d.*)(\·)')
    time_posted_selection = re.search(time_pattern, job_details) 
    if time_posted_selection is not None:
        time_posted = time_posted_selection.group(1)
        return time_posted 

def parse_relative_post_time_to_date(job_details):
    parse_job_time = cut_out_time(job_details)
    cal = parsedatetime.Calendar()
    date = cal.parse(parse_job_time)
    return date

def parsed_date_to_python_date_object(job_details):
    parsed_date = parse_relative_post_time_to_date(job_details)
    year = parsed_date[0][0]
    month = parsed_date[0][1]
    day = parsed_date[0][2]
    hour = parsed_date[0][3] 
    minute = parsed_date[0][4] 
    date_translate = datetime.datetime(year, month, day, hour, minute)
    return date_translate
