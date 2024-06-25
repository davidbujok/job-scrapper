from logging import log
from logger import log_job

def main():

    link_to_job = "some_link"
    job_id = 1
    job_title_text = "Software Engineer"
    company_name_text = "Acme Corp"
    job_location_text = "New York"
    job_description_text = "Job description here"
    ad_date = "2023-10-01"
    id_of_the_website = "indeed"

    data = (link_to_job, job_id, job_title_text, company_name_text, job_location_text,
        job_title_text, job_description_text, ad_date, id_of_the_website, False,
        False)

    log_job("indeed", job_title_text, company_name_text, job_location_text, job_title_text, ad_date)

main()
