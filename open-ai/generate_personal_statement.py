import time
from openai import OpenAI
import psycopg2
from psycopg2.errors import Error

client = OpenAI()

connection = psycopg2.connect(
    database="mydatabase", host="localhost", user="arch", password="", port=5432
)
selected_id = input() 
find_job_position_by_id_query = 'SELECT * FROM jobs WHERE id = %s'
job_id = None
job_level = 'Junior Software Developer'
job_position = None
company_name = None
company_values = None
job_details = None
job_url = None
# second_draft = None
try:
    with connection.cursor() as cursor:
        try:
            job_data = cursor.execute(find_job_position_by_id_query, ( selected_id, ))
            job_id = cursor.fetchall()
            # print('job_level',job_id[0][1])
            # print('job_position',job_id[0][2])
            # print('about_long_section',job_id[0][3])
            # print('job_url',job_id[0][4])
            # print('website_id',job_id[0][5])
            # print('job_id',job_id[0][6])
            # print('job_post_date',job_id[0][7])
            # print('comapny_name',job_id[0][8])
            # print('job_location',job_id[0][9])
        except Exception as e:
            connection.rollback()
            print(f"Error inserting into websites table: {e}")
except Error as e:
    print("Database connection error: ", e)

try:
    if job_id != None:
        job_level = job_id[0][1]
        job_position = job_id[0][2]
        company_name = job_id[0][8]
        company_values = job_id[0][3]
        job_url =  job_id[0][4]
except UnboundLocalError:
    print(f"Job id doesn't exisit")

with open("cv.txt", "r") as cv:
    cv_text = cv.read()

prompt_personal_statement = f"""Considering education and job history of this individaul {cv_text}
who wants to apply for this position: {job_position} of this level: {job_level} for this comapny:
{company_name} write Personal Statement for the CV. When writing the personal statement consider
job details in here: {company_values} and how they align with candidate experiance such as programming
languages and technologies. Focus on the most recent acomplishments of the individaul especially
CodeClan Bootcamp as he's seeking the role as a Junior or Entry Level Software developer. 
Individual also co-developed 'Edinburgh Bin Collection days' application avaliable on mobile 
devices through PlayStore and AppStore.
Try to tie his experiance and soft skill and how they can be helpful for the company, however try 
no to focus on Chef background too much or at at all. Tie softskills skills gained
as a digital assistant to the company values and culture. 
Made Personal statement six to eight sentences focusing mainly on technologies that
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

first_personal_statement = personal_statement.choices[0].message.content

waiting_time = 0
while first_personal_statement is None:
    time.sleep(5)
    waiting_time+=5
    print('Waiting for finishing first task ', waiting_time, ' seconds')

if first_personal_statement is not None:
    second_draft_prompt = f""" Considering this Personal Statment: {first_personal_statement} try to
    improve on it. Create three additional variants of original personal statement. I'm aiming to 
    convey positivity and teamwork and eagerness to improve and learn, traits I believe
    are crucial for contributing to the company's success. """
    second_draft = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {
                "role": "assistant",
                "content": f"{second_draft_prompt}",
            }
        ],
    )

prompt_user_email = f"""Considering position: {job_position}, level of the job: {job_level}, 
company: {company_name} and job details: {company_values} as well as 
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
    if second_draft.choices[0].message.content is not None:
        ps.write(f"ADDITIONAL VARIANTS\n")
        ps.write(second_draft.choices[0].message.content)
    if e_mail.choices[0].message.content is not None:
        ps.write(f"E-MAIL\n")
        ps.write(e_mail.choices[0].message.content)

print(job_url)
