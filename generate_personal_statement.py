from openai import OpenAI
import psycopg2
from psycopg2.errors import Error

client = OpenAI()

connection = psycopg2.connect(
    database="mydatabase", host="localhost", user="arch", password="", port=5432
)
selected_id = 64
find_job_position_by_id_query = 'SELECT * FROM jobs WHERE id = %s'
job_id = None
try:
    with connection.cursor() as cursor:
        try:
            # job_data = cursor.execute(find_job_level_by_id_query, ( selected_id, ))
            # job_data = cursor.execute(find_job_position_by_id_query, ( selected_id, ))
            job_data = cursor.execute(find_job_position_by_id_query, ( selected_id, ))
            job_id = cursor.fetchall()
            print(job_id[0][1])
            print(job_id[0][2])
            print(job_id[0][3])
            print(job_id[0][4])
            # for info in job_id:
            #     print(info)
        except Exception as e:
            connection.rollback()
            print(f"Error inserting into websites table: {e}")
except Error as e:
    print("Database connection error: ", e)

try:
    if job_id != None:
        job_level = job_id[0][1]
        job_position = job_id[0][2]
        company_info  = job_id[0][3]
        job_details  = job_id[0][4]
except UnboundLocalError:
    print(f"Job id doesn't exisit")

with open("cv.txt", "r") as cv:
    cv_text = cv.read()

prompt_personal_statement = f"""Considering education and job history of this individaul {cv_text} who wants to 
apply for this position: {job_position} of this level: {job_level} for this comapny: {company_info}
write Personal Statement for the CV. When writing the personal statement consider job details in 
here: {job_details} and how they align with candidate experiance, programming languages and
technologies. Focus on the most recent acomplishments of the individaul especially CodeClan
Bootcamp as he's seeking the role as a Junior or Entry Level Software developer. 
Try to tie his experiance and soft skill and how they can be helpful for the company in the job 
description. Made Personal statement six to eight sentences focusing mainly on technologies that
individaul knows and how they are tightly connected with technologies in the job description"""


personal_statement = client.chat.completions.create(
    model="gpt-4-1106-preview",
    messages=[
        {
            "role": "assistant",
            "content": f"{prompt_personal_statement}",
        }
    ],
)

prompt_user_email = f"""Considering position: {job_position}, level of the job: {job_level}, 
company: {company_info} and job details: {job_details} as well as 
{personal_statement.choices[0].message.content} write short e-mail that will be send along with cv
to apply for a job"""

e_mail = client.chat.completions.create(
    model="gpt-4-1106-preview",
    messages=[
        {
            "role": "assistant",
            "content": f"{prompt_user_email}",
        }
    ],
)

with open("personal_statement.txt", "w") as ps:
    if personal_statement.choices[0].message.content is not None:
        ps.write(f"PERSONAL STATEMENT\n")
        ps.write(personal_statement.choices[0].message.content)
    if e_mail.choices[0].message.content is not None:
        ps.write(f"E-MAIL\n")
        ps.write(e_mail.choices[0].message.content)


# # print(completion)
# # print(type(completion))
# __import__("pprint").pprint(f"{ personal_statement.choices[0].message.content }")
print("Completed")
