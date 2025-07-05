import requests
from bs4 import BeautifulSoup
import json

def get_build_id():
    """
    Scrape the buildId from the HTML script tag to construct grant API URLs dynamically.
    """
    url = "https://www.find-government-grants.service.gov.uk/grants"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    script_tag = soup.find("script", id="__NEXT_DATA__")
    data = json.loads(script_tag.string)
    return data["buildId"]

def fetch_all_grants(build_id, total_pages=9, page_size=10):
    """
    Fetch grant data from the Next.js JSON endpoints using the dynamic build_id.
    Returns a list of grants, each with an added 'url' key for the grant page.
    """
    base_url = f"https://www.find-government-grants.service.gov.uk/_next/data/{build_id}/en/grants.json"
    
    all_grants = []

    for page in range(1, total_pages + 1):
        if page == 1:
            url = base_url
        else:
            skip = (page - 1) * page_size
            url = f"{base_url}?skip={skip}&limit={page_size}&page={page}"
        
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch page {page}: {response.status_code}")
            continue

        data = response.json()
        grants = data.get('pageProps', {}).get('searchResult', [])
        
        for grant in grants:
            grant_url = f"https://www.find-government-grants.service.gov.uk/grants/{grant['label']}"
            grant['url'] = grant_url
            all_grants.append(grant)
        
        print(f"Page {page}: {len(grants)} grants found.")

    return all_grants
