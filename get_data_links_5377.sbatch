#!/bin/bash
#SBATCH -A egodat_oit_research_tech_0001
#SBATCH -D /users/mlangstonsmith/milesplit-scraper/
#SBATCH -J get_data_links
#SBATCH -o /users/mlangstonsmith/milesplit-scraper/debug/output-%j.txt
#SBATCH -e /users/mlangstonsmith/milesplit-scraper/debug/error-%j.txt
#SBATCH -p fp-gpgpu-3
#SBATCH -t 7-00:00:00
#SBATCH --mem=20G
#SBATCH -c 1
#SBATCH -G 1

mkdir -p debug

module load conda
conda activate milesplit

python /users/mlangstonsmith/milesplit-scraper/get_data_links_5377.py --start 5377 --end 5377