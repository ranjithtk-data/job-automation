KEYWORDS = [
    "data analyst",
    "business analyst",
    "mis analyst",
    "data analytics",
    "business intelligence"
]

def filter_jobs(jobs):

    filtered = []

    for job in jobs:

        title = job["title"].lower()

        if any(keyword in title for keyword in KEYWORDS):
            filtered.append(job)

    return filtered
