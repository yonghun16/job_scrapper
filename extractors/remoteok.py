from bs4 import BeautifulSoup
import requests

def extract_remoteok_jobs(term):
  url = f"https://remoteok.com/remote-{term}-jobs"
  request = requests.get(url, headers={"User-Agent": "Kimchi"})
  results = []
  if request.status_code == 200:
    soup = BeautifulSoup(request.text, "html.parser")
    jobs = soup.find_all('tr', class_="job")
    for job in jobs:
        position = job.find('h2', itemprop="title").string.strip()
        company = job.find('h3', itemprop="name").string.strip()
        location = job.find('div', class_="location").string.strip()
        links = job.find("a", itemprop="url")
        link = f"https://remoteok.com/{links['href']}"
        search = {
            'position' : position,
            'company' : company,
            'location' : location,
            'link' : link
        }
        results.append(search)
  else:
    print("Can't get jobs.")
  return results
