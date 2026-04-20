import feedparser

def scrape_jobs():

    feeds = [
        "https://in.indeed.com/rss?q=data+analyst&l=Bengaluru",
        "https://www.naukri.com/data-analyst-jobs-in-bangalore?format=rss"
    ]

    jobs = []

    for url in feeds:

        feed = feedparser.parse(url)

        for entry in feed.entries[:15]:

            jobs.append({
                "title": entry.title,
                "company": entry.get("author", "Company"),
                "location": "Bengaluru",
                "link": entry.link
            })

    return jobs
