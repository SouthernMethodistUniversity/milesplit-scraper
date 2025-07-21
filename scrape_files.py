import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import re
import math
import time
import random
from io import StringIO
from datetime import date
import pickle
import re
import os
import hashlib

def get_file_hash(file_path, algo='sha256'):
    hasher = hashlib.new(algo)
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


# == Setup initial directories and get data files

directory = "data/"
files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

o_dir = "text_files/"
os.makedirs(o_dir, exist_ok=True)

print(files)

if os.path.exists(f"{o_dir}md5s.pkl"):
    with open(f"{o_dir}md5s.pkl", "rb") as f:
        md5s = pickle.load(f)
else:
    md5s = []

if os.path.exists(f"{o_dir}metadata.pkl"):
    with open(f"{o_dir}metadata.pkl", "rb") as f:
        metadata = pickle.load(f)
else:
    columns = ['meet_link', 'results_link', 'meet_name', 'meet_date', 'venue_name', 'venue_link', 'venue_city', 'filepath', 'hash', 'is_duplicate']
    metadata = pd.DataFrame(columns=columns)

for file in files:
    with open(f"{directory}{file}", "rb") as f:
        tmp_links = pickle.load(f)

    i = 0

    for k in tmp_links:
        i = i + 1
        # == Create directories ==
        kclean = re.sub(r'[^a-zA-Z0-9-]', '_', k)
        print(k)
        os.makedirs(f"{o_dir}{kclean}", exist_ok=True)
        for l in tmp_links[k]:

            if l not in list(metadata['results_link']):

                row_data = {
                    'meet_link': k,
                    'results_link': l,
                    'meet_name': None,
                    'meet_date': None,
                    'venue_name': None,
                    'venue_link': None,
                    'venue_city': None,
                    'filepath': None,
                    'hash': None,
                    'is_duplicate': None
                }

                #lclean = re.sub(r'[^a-zA-Z0-9-]', '_', l).split(re.sub(r'[^a-zA-Z0-9-]', '_', k))[1]
                #if i < 6:
                #    print("\t", lclean)

                r = requests.get(l)
                soup = BeautifulSoup(r.content, 'html.parser')
                tags = soup.select("pre")
                print("\t\t", soup.select("h1.meetName")[0].get_text().strip())
                print("\t\t", soup.select("div.date time")[0].get_text().strip())
                print("\t\t", soup.select("div.venueName")[0].get_text().strip())
                print("\t\t", soup.select("div.venueName a")[0].get("href").strip())
                print("\t\t", soup.select("div.venueCity")[0].get_text().strip())

                row_data['meet_name'] = soup.select("h1.meetName")[0].get_text().strip()
                row_data['meet_date'] = soup.select("div.date time")[0].get_text().strip()
                row_data['venue_name'] = soup.select("div.venueName")[0].get_text().strip()
                row_data['venue_city'] = soup.select("div.venueCity")[0].get_text().strip()

                #with open(file, "w", encoding="utf-8") as f:
                #    for tag in tags:
                #        f.write(tag.get_text())
                #        f.write("\n\n")
                #hash_value = get_file_hash(file, algo='sha256')
                #print("SHA-256:", hash_value)
                tag_combo = "\n".join(tag.get_text() for tag in tags)
                hash_object = hashlib.md5(tag_combo.encode('utf-8'))
                hash_hex = hash_object.hexdigest()
                print("MD5:", hash_hex)
                row_data['hash'] = hash_hex
                if hash_hex in md5s and os.path.exists(f"{o_dir}{kclean}/{hash_hex}.txt"):
                    print("\n -- Skipping file, already exists")
                    row_data['is_duplicate'] = True
                    result = metadata.loc[metadata['hash'] == hash_hex, 'filepath']
                    if not result.empty:
                        row_data['filepath'] = result.iloc[0]
                    else:
                        row_data['filepath'] = None
                else:
                    with open(f"{o_dir}{kclean}/{hash_hex}.txt", "w", encoding="utf-8") as f:
                        f.write(tag_combo)
                    md5s.append(hash_hex)
                    print(f"\n✅ NEW FILE CREATED: {o_dir}{kclean}/{hash_hex}.txt")
                    row_data['is_duplicate'] = False
                    row_data['filepath'] = f"{o_dir}{kclean}/{hash_hex}.txt"
                
                metadata.loc[len(metadata)] = row_data
                #else:
                #print("SKIPPED")

print(md5s)
with open(f"{o_dir}md5s.pkl", "wb") as f:
    pickle.dump(md5s, f)

print(metadata)
with open(f"{o_dir}metadata.pkl", "wb") as f:
    pickle.dump(metadata, f)