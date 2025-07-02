import requests
from bs4 import BeautifulSoup
import pickle

# === Set ranges ===
base_url = "https://www.milesplit.com/results/?"
years = [str(x) for x in list(range(2006,2026))]
months = [str(x) for x in list(range(1,13))]
levels = ["hs"]

# === Scrape links ===
links = []
for l in levels:
    for y in years:
        for m in months:
            url = base_url + "month=" + m + "&year=" + y + "&level=" + l
            print(url)
            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'html.parser')
            tags = soup.select("td.name a")
            hrefs = [a['href'] for a in tags if 'href' in a.attrs]
            links.extend(hrefs)

# === Save to pickle file ===
with open("meet_links.pkl", "wb") as f:
    pickle.dump(links, f)

print(f"\n✅ Saved {len(links)} links to 'meet_links.pkl'")