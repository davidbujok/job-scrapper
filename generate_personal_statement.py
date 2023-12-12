from os import close
from openai import OpenAI 
import pprint
client = OpenAI()

jobs = open("job_offers.txt", "r")
jobs_sorted = []
job = ""
for line in jobs:
    if line.startswith("---"):
        jobs_sorted.append(job)
        job = ""
        pass
    else:
        job += f"{line.strip()} \n"

print(len(jobs_sorted))
print(jobs_sorted[0])
print("-----------------------------------------------------------------")
jobs.close()
cv = open("cv.txt", "r")
cv_text = ""
for line in cv:
    cv_text += line

prompt_user = "Considering education and job history of the individaul below and job description write Personal Statement for the CV. Focus on the most recent acomplishments of the individaul especially CodeClan Bootcamp as he's seeking the role as a Junior Software developer. Try to tie his experiance and soft skill and how they can be helpful for the company in the job description. Made Personal statement six to eight sentences focusing mainly on technologies that individaul knows and how they are tightly connected with technologies in the job description"


completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": f"{prompt_user} CV: {cv_text} and here's job description {jobs_sorted[0]}"}
    ]
)

# print(completion)
# print(type(completion))
__import__('pprint').pprint(f"{ completion.choices[0].message.content }")
