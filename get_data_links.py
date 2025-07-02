import requests
from bs4 import BeautifulSoup
import pickle
import argparse
import os
import sys

parser = argparse.ArgumentParser(description="Subset the links list.")
parser.add_argument("--start", type=int, default=0, help="Start index (inclusive)")
parser.add_argument("--end", type=int, default=0, help="End index (inclusive)")
parser.add_argument("--output", type=str, default=None, help="Name of .pkl output file")
args = parser.parse_args()

if args.start is None or args.end is None:
    print("❌ Error: You must provide both --start and --end.")
    sys.exit(1)

os.chdir("/users/mlangstonsmith/milesplit-scraper/")

with open("/users/mlangstonsmith/milesplit-scraper/meet_links.pkl", "rb") as f:
    links = pickle.load(f)

args.end = min(len(links)-1, args.end)

links_subset = links[args.start:args.end+1]

raw_links = dict()

for l in links_subset:
    raw = []
    print(f"Scraping: {l}")
    try:
        r = requests.get(l)
        r.raise_for_status()
    except Exception as e:
        print(f"Failed to fetch {l}: {e}")
        continue

    soup = BeautifulSoup(r.content, 'html.parser')
    tags = soup.select("a")
    hrefs = [a['href'] for a in tags if 'href' in a.attrs]

    for h in hrefs:
        if h.startswith("https://"):
            try:
                resp = requests.get(h, allow_redirects=True)
                final_url = resp.url

                if "raw" in final_url:
                    #print("---", final_url)
                    raw.append(final_url)
                else:
                    # One level deeper: scrape this page too
                    try:
                        soup2 = BeautifulSoup(resp.content, 'html.parser')
                        deeper_links = [a['value'] for a in soup2.select("option") if 'value' in a.attrs]
                        #print(deeper_links)

                        for d in deeper_links:
                            if "milesplit" in d:
                                #print("- Scraping:", d)
                                try:
                                    d_resp = requests.get(d, allow_redirects=True)
                                    d_final_url = d_resp.url

                                    if "raw" in d_final_url:
                                        #print("------", d_final_url)
                                        raw.append(d_final_url)
                                except Exception as e:
                                    print(f"Error in second-level follow {d}: {e}")
                    except Exception as e:
                        print(f"Failed to parse second-level page: {e}")

            except Exception as e:
                print(f"Error following {h}: {e}")
    if raw:
        raw_links[l] = list(set(raw))
        print("---", len(raw_links[l]))
    else:
        raw_links[l] = [l]
        print("---", "NONE, Setting link to original.")

# === Save to pickle file ===
output_dir = "/users/mlangstonsmith/milesplit-scraper/data/"
os.makedirs(output_dir, exist_ok=True)

if args.output == None:
    with open(f"data/data_links_{args.start}_{args.end}.pkl", "wb") as f:
        pickle.dump(raw_links, f)

    print(f"\n✅ Saved links to 'data/data_links_{args.start}_{args.end}.pkl'")
else:
    with open(f"data/{args.output}", "wb") as f:
        pickle.dump(raw_links, f)

    print(f"\n✅ Saved links to 'data/{args.output}'")