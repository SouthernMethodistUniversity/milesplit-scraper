import requests
from bs4 import BeautifulSoup
import pickle
import argparse
import os
import sys
import time

parser = argparse.ArgumentParser(description="Subset the links list.")
parser.add_argument("--start", type=int, default=0, help="Start index (inclusive)")
parser.add_argument("--end", type=int, default=0, help="End index (inclusive)")
parser.add_argument("--output", type=str, default=None, help="Name of .pkl output file")
args = parser.parse_args()

if args.start is None or args.end is None:
    print("❌ Error: You must provide both --start and --end.")
    sys.exit(1)

os.chdir("/users/mlangstonsmith/milesplit-scraper/")

with open("meet_links.pkl", "rb") as f:
    links = pickle.load(f)

args.end = min(len(links)-1, args.end)
links_subset = links[args.start:args.end+1]

raw_links = dict()
start_time = time.time()
TIME_LIMIT = 23 * 3600  # 23 hours in seconds

i = 0

for l in links_subset:

    time.sleep(5)
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
        if h.startswith("https://") and "milesplit" in h:
            try:
                time.sleep(5)
                resp = requests.get(h, allow_redirects=True)
                final_url = resp.url

                if "raw" in final_url:
                    raw.append(final_url)
                else:
                    try:
                        soup2 = BeautifulSoup(resp.content, 'html.parser')
                        deeper_links = [a['value'] for a in soup2.select("option") if 'value' in a.attrs]
                        for d in deeper_links:
                            if "milesplit" in d:
                                try:
                                    time.sleep(5)
                                    d_resp = requests.get(d, allow_redirects=True)
                                    d_final_url = d_resp.url
                                    if "raw" in d_final_url:
                                        raw.append(d_final_url)
                                except Exception as e:
                                    print(f"Error in second-level follow {d}: {e}")
                    except Exception as e:
                        print(f"Failed to parse second-level page: {e}")
            except Exception as e:
                print(f"Error following {h}: {e}")

    raw_links[l] = list(set(raw)) if raw else [l]
    print("---", len(raw_links[l]) if raw else "NONE, Setting link to original.")
    index_completed = args.start + i
    partial_output = f"data_links_{args.start}_{index_completed}_partial.pkl"
    with open(f"/lustre/scratch/client/users/mlangstonsmith/milesplit_partials/{partial_output}", "wb") as f:
        pickle.dump(raw_links, f)
    print(f"✅ Partial save completed to data/{partial_output}")
    i = i + 1

# === Final Save ===
output_dir = "data/"
os.makedirs(output_dir, exist_ok=True)

output_path = f"{output_dir}/{args.output}" if args.output else f"{output_dir}/data_links_{args.start}_{args.end}.pkl"
with open(output_path, "wb") as f:
    pickle.dump(raw_links, f)

print(f"\n✅ Saved links to '{output_path}'")
