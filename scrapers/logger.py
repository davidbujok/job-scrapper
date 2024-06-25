import os

def log_job(website, job_title_text, company, location, job_header_level, ad_date):
    try:
        # Open the log file in append mode
        with open("log.txt", "a") as log:
            log.write(f"{job_title_text}, {job_header_level} for {company} in {location} Date: ** {ad_date} ** >>{website}<<\n")
        print(f"Logged job: {job_title_text}, {company} in {location}")
    except Exception as e:
        # Print the error if occurs
        print(f"Error logging job: {e}")

