#!/bin/bash
#SBATCH -A egodat_oit_research_tech_0001
#SBATCH -D /users/mlangstonsmith/milesplit-scraper/
#SBATCH -J get_data_links
#SBATCH -o /users/mlangstonsmith/milesplit-scraper/debug/output-%j.txt
#SBATCH -e /users/mlangstonsmith/milesplit-scraper/debug/error-%j.txt
#SBATCH -p htc
#SBATCH -t 1-00:00:00
#SBATCH --mem=10G

mkdir -p debug

module load conda
conda activate milesplit

python /users/mlangstonsmith/milesplit-scraper/get_data_links.py --start 91 --end 200