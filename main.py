from email_sender import send_email

keywords = [
"data analyst",
"mis analyst",
"mis executive",
"power bi analyst",
"sql analyst",
"reporting analyst",
"business analyst fresher"
]

job_links = []

def linkedin_jobs():
    for k in keywords:
        link = f"https://www.linkedin.com/jobs/search/?keywords={k.replace(' ','%20')}&location=Bengaluru&f_E=2"
        job_links.append(f"LinkedIn – {k}\n{link}")

def indeed_jobs():
    for k in keywords:
        link = f"https://in.indeed.com/jobs?q={k.replace(' ','+')}&l=Bangalore"
        job_links.append(f"Indeed – {k}\n{link}")

def naukri_jobs():
    for k in keywords:
        link = f"https://www.naukri.com/{k.replace(' ','-')}-jobs-in-bangalore"
        job_links.append(f"Naukri – {k}\n{link}")

def company_careers():

    companies = {
        "Accenture":"https://www.accenture.com/in-en/careers/jobsearch",
        "Wipro":"https://careers.wipro.com",
        "Cognizant":"https://careers.cognizant.com",
        "Capgemini":"https://www.capgemini.com/careers",
        "Deloitte":"https://jobs.deloitte.com",
        "EY":"https://careers.ey.com",
        "KPMG":"https://home.kpmg/in/en/home/careers.html",
        "JP Morgan":"https://careers.jpmorgan.com"
    }

    for name,link in companies.items():
        job_links.append(f"{name} Careers\n{link}")

def main():

    linkedin_jobs()
    indeed_jobs()
    naukri_jobs()
    company_careers()

    unique_jobs = list(set(job_links))

    jobs_text = "\n\n".join(unique_jobs)

    send_email(
        "Daily Data Analyst / MIS Jobs – Bangalore",
        jobs_text
    )

if __name__ == "__main__":
    main()
