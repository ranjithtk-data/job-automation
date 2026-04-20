import feedparser

def scrape_jobs():

    feeds = [
        "https://in.indeed.com/rss?q=data+analyst&l=Bengaluru",
        "https://in.indeed.com/rss?q=business+analyst&l=Bengaluru",
        "https://www.naukri.com/data-analyst-jobs-in-bangalore?format=rss"
    ]

    jobs = []

    for feed_url in feeds:

        feed = feedparser.parse(feed_url)

        for entry in feed.entries[:20]:

            jobs.append({
                "title": entry.title,
                "company": entry.get("author", "Company"),
                "location": "Bengaluru",
                "link": entry.link
            })

    return jobs
