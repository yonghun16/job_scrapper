from bs4 import BeautifulSoup
import requests


def extract_workremotely_jobs(term):
    url = f"https://weworkremotely.com/remote-jobs/search?&term={term}"
    request = requests.get(url, headers={"User-Agent": "Kimchi"})
    results = []
    if request.status_code == 200:
        soup = BeautifulSoup(request.text, "html.parser")
        jobs = soup.find_all("section", class_="jobs")
        for job in jobs:
            job_posts = job.find_all('li')
            job_posts.pop(-1)
            for post in job_posts:
                company = post.find_all("span", class_="company")[0]
                position = post.find("span", class_="title")
                location = post.find("span", class_="region")
                link = post.find("a", reculsive=False)
                if company:
                    company = company.string.strip()
                if position:
                    position = position.string.strip()
                if location:
                    location = location.string.strip()
                if link:
                    link = f"https://weworkremotely.com/{link['href']}"
                if company and position and location and link:
                    job = {
                        'company': company,
                        'position': position,
                        'location': location,
                        'link': link
                    }
                    results.append(job)
    else:
        print("Can't get jobs.")
    return results
