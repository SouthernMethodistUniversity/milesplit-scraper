# MileSplit Scraper

With permission from FloSports, the parent company of MileSplit, the following 
process was used to scrape 20 years of cross country and track and field meet data.

## Setup

The `requirements.txt` flag can be used to build an environment with the
necessary packages in Python using common methods for building environments, such
as conda or venv.

## Step 1: Getting the Meet Links

In the script titled [get_meet_links.py](get_meet_links.py), the [index page](https://www.milesplit.com/results)
was scraped for links to each meet that occured from January 2006 to June 2025. This script could
be used to get additional meet links past June 2025 if needed. The results are saved 
in [meet_links.pkl](meet_links.pkl), which is a Python native format for storing objects.
The following code can be used to load the file:

```python
import pickle
with open("meet_links.pkl", "rb") as f:
        meet_links = pickle.load(f)
```

## Step 2: Finding the Raw Data Pages

Each meet has various "raw" data pages that contain all of the data output from time
tracking software. Depending on the state/institution/software, the output may be split onto 
different pages. The collection of files starting with `get_data_links` are used in conjunction
with the SLURM job scheduler on SMUs supercomputer, [M3](https://www.smu.edu/oit/services/m3) to
find the links on each page. 

Each meet took anywhere from 1 minute to 7 days to scrape for links.
The methodology used in finding these links was to look for pages with the word "raw" in the link,
since various URL formats were used to map to the raw data. A buffer was added between checks on
the links in order to not overwhelm MileSplit servers.

One meet, which split the raw data onto many pages, exceeded the limit of 7 days on M3, so custom code
was written in [get_data_links_5377.py](get_data_links_5377.py) accounting for the URL formatting used
in that case.

The `sbatch` files in conjunction with [setup_jobs.sh](setup_jobs.sh) were used to chunk
links into sets of 100 meets to process. The output of each run is a `.pkl` file with a list of links
and what meet they correspond to.

## Step 3: Scraping the Raw Data

Each `.pkl` file that resulted from a run on M3 was offloaded to a laptop to then scrape the raw data
from each page into `.txt` files for further processing. The file called [scrape_files.py](scrape_files.py)
takes arguments for input and output directories, and can process multiple `.pkl` files at once. All results
can be found in compressed folders containing the `.pkl` files, the `.txt` results and a `metadata.pkl` file
with information about the meets at [this Box link](https://smu.app.box.com/folder/332105550889).

## Step 4: Data Processing

This step was done by students working under Benjamin Williams at University of Denver and is not documented
in this repository.